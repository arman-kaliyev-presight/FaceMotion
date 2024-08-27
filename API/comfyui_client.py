import websocket  # NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import json
import urllib.request
import urllib.parse
import uuid
import logging
from PIL import Image
import shutil
import os
from fastapi import File
from API.workflow_prompt import params

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

server_address = "127.0.0.1:8188"

directory_output = '/home/armankk/dev/LivePortraitComfUI/ComfyUI/output/'
directory_input = '/home/armankk/dev/LivePortraitComfUI/ComfyUI/input/'


def save_file(file_to_save: File):
    video_path = directory_input + file_to_save.filename
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file_to_save.file, buffer)
    return video_path


def save_image(image):
    file_name = "input_image.jpeg"
    im = Image.fromarray(image)
    im.save(directory_input + file_name)
    return file_name


class ComfyUIClient:
    def __init__(self, client_id, server_address):
        self.client_id = client_id
        self.server_address = server_address

        self.ws = websocket.WebSocket()
        self.ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))

    def queue_prompt(self, prompt):
        p = {"prompt": prompt, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request("http://{}/prompt".format(self.server_address), data=data)
        return json.loads(urllib.request.urlopen(req).read())

    def get_file(self, filename, subfolder, folder_type):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen("http://{}/view?{}".format(self.server_address, url_values)) as response:
            return response.read()

    def get_history(self, prompt_id):
        with urllib.request.urlopen("http://{}/history/{}".format(self.server_address, prompt_id)) as response:
            return json.loads(response.read())

    def get_images(self, prompt):
        prompt_id = self.queue_prompt(prompt)['prompt_id']
        output = {}
        while True:
            out = self.ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message['type'] == 'executing':
                    data = message['data']
                    if data['node'] is None and data['prompt_id'] == prompt_id:
                        break  # Execution is done
            else:
                continue  # previews are binary data

        history = self.get_history(prompt_id)[prompt_id]
        for node_id, node_output in history['outputs'].items():
            if 'gifs' in node_output:
                for node_file in node_output['gifs']:
                    filename = node_file['filename']
                    file_data = self.get_file(filename, node_file['subfolder'], node_file['type'])
                    output[filename] = file_data

        return output


def put_motion_to_photo(image, video_path):
    client_id = str(uuid.uuid4())
    client = ComfyUIClient(client_id=client_id, server_address=server_address)
    if directory_input not in video_path:
        dst = shutil.copy(video_path, directory_input)
    else:
        dst = video_path
    video_file_name = os.path.basename(dst)
    image_file_name = save_image(image)

    logger.info(f"Start video analysis of {video_file_name}")
    logger.info(f"Start image analysis of {image_file_name}")

    prompt_params = params.copy()
    prompt_params["4"]["inputs"]["image"] = image_file_name
    prompt_params["5"]["inputs"]["video"] = video_file_name
    outputs = client.get_images(prompt_params)
    names = list(outputs.keys())
    if len(names) > 0:
        logger.info(f"Conversion succeed, file {names[0]}")
        return directory_output + names[0]
    else:
        logger.info(f"Conversion did not succeed, return empty result")
        return None

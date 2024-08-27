import io
import numpy as np
import logging
from PIL import Image
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, Response
from API.comfyui_client import put_motion_to_photo, save_file

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

app = FastAPI()


@app.post("/comfyui/photo/motion")
async def process_files(image: UploadFile = File(...), video: UploadFile = File(...)):
    logger.info("Received request to process files")

    try:
        image_bytes = await image.read()
        image_pil = Image.open(io.BytesIO(image_bytes))
        image_np = np.array(image_pil)
        logger.info("Image successfully converted to NumPy array")

        # Save the uploaded video file
        video_path = save_file(video)
        logger.info(f"Video saved to {video_path}")

        # Process the video with the image
        output_video_path = put_motion_to_photo(image_np, video_path)
        logger.info(f"Video processing completed, output saved to {output_video_path}")

        # Return the processed video file
        return FileResponse(output_video_path, media_type='video/mp4', filename='processed_video.mp4')

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return Response(status_code=200)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

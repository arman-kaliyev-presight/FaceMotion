import gradio as gr
from API.comfyui_client import put_motion_to_photo

with gr.Blocks() as demo:
    with gr.Row():
        input_image = gr.Image(label="Target Image",
                               height=360,
                               width=540)
        input_video = gr.Video(label="Source Video",
                               height=360,
                               width=540)
        output_video = gr.Video(label="Output Result",
                                height=360,
                                width=540)
    with gr.Row():
        with gr.Column(scale=1):
            pass

        with gr.Column(scale=1):
            with gr.Row():
                apply_button = gr.Button("Apply", size="sm", variant="primary")
                clear_btn = gr.ClearButton(components=[input_image, input_video, output_video], size="sm")

        with gr.Column(scale=1):
            pass

    apply_button.click(put_motion_to_photo, inputs=[input_image, input_video], outputs=output_video)
    clear_btn.click()

if __name__ == "__main__":
    demo.launch()

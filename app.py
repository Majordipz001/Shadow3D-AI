import random
import gradio as gr
from gradio_client import Client, handle_file

SPACE_ID = "microsoft/TRELLIS.2"

# These are the current default settings used by the official TRELLIS.2 demo.
DEFAULTS = {
    "resolution": "512",  # Start small to reduce wait time.
    "ss_guidance_strength": 7.5,
    "ss_guidance_rescale": 0.7,
    "ss_sampling_steps": 12,
    "ss_rescale_t": 5.0,
    "shape_slat_guidance_strength": 7.5,
    "shape_slat_guidance_rescale": 0.5,
    "shape_slat_sampling_steps": 12,
    "shape_slat_rescale_t": 3.0,
    "tex_slat_guidance_strength": 1.0,
    "tex_slat_guidance_rescale": 0.0,
    "tex_slat_sampling_steps": 12,
    "tex_slat_rescale_t": 3.0,
}

def get_client():
    # Uses the public Hugging Face Space. It runs the heavy model remotely,
    # so your phone/laptop does not need a powerful GPU for generation.
    return Client(SPACE_ID)

def find_endpoint(client, preferred):
    """Find an endpoint by its name, tolerating leading slashes."""
    info = client.view_api(return_format="dict")
    endpoints = info.get("named_endpoints", {})
    for name in endpoints:
        clean = name.lstrip("/")
        if clean == preferred or preferred in clean:
            return name
    available = ", ".join(endpoints.keys()) or "No named endpoints returned"
    raise RuntimeError(
        f"Couldn't find the '{preferred}' endpoint in the public demo. "
        f"Available endpoints: {available}. The demo API may have changed."
    )

def generate_3d(image, resolution):
    if image is None:
        raise gr.Error("Upload a clear image first. A single character/object on a plain background works best.")
    try:
        client = get_client()
        endpoint = find_endpoint(client, "image_to_3d")
        seed = random.randint(1, 2_000_000_000)
        args = [
            handle_file(image), seed, resolution,
            DEFAULTS["ss_guidance_strength"],
            DEFAULTS["ss_guidance_rescale"],
            DEFAULTS["ss_sampling_steps"],
            DEFAULTS["ss_rescale_t"],
            DEFAULTS["shape_slat_guidance_strength"],
            DEFAULTS["shape_slat_guidance_rescale"],
            DEFAULTS["shape_slat_sampling_steps"],
            DEFAULTS["shape_slat_rescale_t"],
            DEFAULTS["tex_slat_guidance_strength"],
            DEFAULTS["tex_slat_guidance_rescale"],
            DEFAULTS["tex_slat_sampling_steps"],
            DEFAULTS["tex_slat_rescale_t"],
        ]
        result = client.predict(*args, api_name=endpoint)
        if not isinstance(result, (list, tuple)) or len(result) < 1:
            raise RuntimeError(f"Unexpected response from the 3D service: {result}")
        model_state = result[0]
        preview_html = result[1] if len(result) > 1 else "<p>Generation complete. Continue to GLB export.</p>"
        return model_state, preview_html, "3D shape generated. Now click **Extract GLB** to create the downloadable model."
    except Exception as exc:
        raise gr.Error(
            "The free shared 3D service may be busy, unavailable, or its API may have changed.\n\n"
            f"Details: {exc}\n\n"
            "Try again later, or use the official demo link in the app."
        )

def export_glb(model_state, face_target, texture_size):
    if model_state is None:
        raise gr.Error("Generate a 3D model before exporting.")
    try:
        client = get_client()
        endpoint = find_endpoint(client, "extract_glb")
        result = client.predict(
            model_state, int(face_target), int(texture_size), api_name=endpoint
        )
        # The official Space returns the GLB path twice (model viewer + download).
        file_path = result[-1] if isinstance(result, (list, tuple)) else result
        if not file_path:
            raise RuntimeError(f"No downloadable file was returned: {result}")
        return file_path, "GLB export complete. Save the file, then open it in Blender."
    except Exception as exc:
        raise gr.Error(
            "GLB export did not complete. The free shared service may have timed out or changed.\n\n"
            f"Details: {exc}\n\n"
            "Try generating again at 512 resolution, or use the official demo link."
        )

def clear_all():
    return None, None, None, None, "Ready. Upload one clear reference image to begin."

with gr.Blocks(title="Shadow3D AI Studio", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🧊 Shadow3D AI Studio — Starter
        **Image → 3D model → GLB download → Blender polishing**

        This is your own simple control panel. The actual 3D generation runs on
        Microsoft's public TRELLIS.2 Hugging Face demo, not on your phone.
        """
    )
    with gr.Row():
        with gr.Column(scale=1):
            image = gr.Image(
                label="Upload a character or object reference",
                type="filepath",
                sources=["upload", "clipboard"],
                height=360,
            )
            resolution = gr.Radio(
                ["512", "1024", "1536"],
                value="512",
                label="Generation resolution",
                info="Start with 512. Higher resolutions may take longer or fail when the free server is busy.",
            )
            generate_btn = gr.Button("✨ Generate 3D shape", variant="primary")
            gr.Markdown(
                """
                **Reference image tips**
                - Use one full-body character or one object.
                - Show the whole subject, including feet and hair.
                - Use a plain/clean background where possible.
                - A front-facing, neutral pose is easiest to reconstruct.
                """
            )
        with gr.Column(scale=1):
            preview = gr.HTML(label="Generation preview")
            status = gr.Markdown("Ready. Upload one clear reference image to begin.")
            face_target = gr.Slider(
                100000, 500000, value=300000, step=10000,
                label="Target polygon count (approx.)"
            )
            texture_size = gr.Radio(
                [1024, 2048, 4096], value=2048, label="Texture resolution"
            )
            export_btn = gr.Button("📦 Extract downloadable GLB")
            download = gr.File(label="Your 3D model (GLB)")
    state = gr.State(None)

    generate_btn.click(
        generate_3d,
        inputs=[image, resolution],
        outputs=[state, preview, status],
    )
    export_btn.click(
        export_glb,
        inputs=[state, face_target, texture_size],
        outputs=[download, status],
    )
    gr.Markdown(
        """
        ---
        **Important:** This starter currently converts an uploaded image into a 3D asset.
        It does not yet create a 3D character directly from text, and TRELLIS.2 is an
        object/image-to-3D system rather than a complete humanoid avatar rigging tool.
        Generated models may need substantial cleanup in Blender before client delivery.
        """
    )

if __name__ == "__main__":
    demo.queue(max_size=8).launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860))
    )

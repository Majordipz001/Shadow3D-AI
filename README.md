# Shadow3D AI Studio — Starter ZIP

A beginner-friendly local control panel for image-to-3D generation.

## What it does
1. You upload one clear image of a character or object.
2. The app sends it to the public Microsoft TRELLIS.2 demo on Hugging Face.
3. The remote service generates a 3D shape.
4. You request a GLB export and download the result.
5. You can then import the GLB into Blender for further work.

## Important limitations
- This is a starter application, not a newly trained AI model.
- It currently supports **image-to-3D**, not direct text-to-3D.
- Heavy generation runs on a public, shared cloud demo. Availability, queue times,
  rate limits and free access can change. No unlimited free generation is promised.
- The public Space's API can change. If it does, the app may need an update.
- TRELLIS.2's repository is MIT-licensed, but always check the licence and terms
  of any model, reference image, generated output and service you use in a client job.
- A generated mesh is not automatically a production-ready humanoid/VRChat avatar.
  It may need retopology, UV work, rigging, weight painting, facial setup and testing.
- Do not upload private or sensitive images to public demo services.

## Windows 10 setup
1. Install Python 3.10 or newer from https://www.python.org/downloads/
   During installation, tick **Add Python to PATH**.
2. Extract this ZIP to a normal folder, for example `Desktop\Shadow3D_AI_Starter`.
3. Double-click `run_windows.bat`.
4. Wait for packages to install. The first setup needs an internet connection.
5. When the terminal shows a local address such as `http://127.0.0.1:7860`,
   open it in Chrome.
6. Upload one clear reference image, keep resolution at 512, and click Generate.
7. When the generation preview appears, click **Extract downloadable GLB**.
8. Download the GLB and open it in Blender.

## Phone use
This app is designed to run on the Windows laptop. Your Redmi phone can open
the official Hugging Face demo directly in Chrome, but running this local Python
app on Android is not the recommended beginner setup.

## Official generation demo
https://huggingface.co/spaces/microsoft/TRELLIS.2

## Project links
- TRELLIS.2 code/model: https://github.com/microsoft/TRELLIS.2
- Blender: https://www.blender.org/
- Gradio: https://www.gradio.app/

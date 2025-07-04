# AI Text-to-Video Generator

Create stunning videos from text descriptions using Runway's AI API.

## Features

- 🎬 Web interface with Streamlit
- 📱 Command line interface
- ⚙️ Customizable video settings
- 📥 Automatic video download
- 🔄 Real-time progress tracking
- 🎯 Advanced prompt optimization

## Installation

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd runway-text-to-video
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env and add your Runway API key
```

4. **Install the package (optional):**
```bash
pip install -e .
```

## Usage

### Web Interface

Launch the Streamlit web app:
```bash
streamlit run runway_text_to_video.py
```

Navigate to `http://localhost:8501` in your browser.

### Command Line

Generate a video directly from the command line:
```bash
python runway_text_to_video.py \
  --api-key YOUR_API_KEY \
  --prompt "A serene lake at sunset with mountains in the background" \
  --duration 6 \
  --resolution 1920x1080 \
  --output my_video.mp4
```

### Python API

Use the client in your own Python code:
```python
from runway_text_to_video import RunwayTextToVideo

# Initialize client
client = RunwayTextToVideo("your_api_key")

# Generate video
result = client.generate_video(
    text_prompt="A butterfly landing on a flower",
    duration=4,
    resolution="1280x768"
)

# Wait for completion
final_result = client.wait_for_completion(result["id"])

# Download video
client.download_video(final_result["video_url"], "butterfly.mp4")
```

## Configuration

### Environment Variables

- `RUNWAY_API_KEY`: Your Runway API key (required)
- `DEFAULT_RESOLUTION`: Default video resolution (optional)
- `DEFAULT_DURATION`: Default video duration in seconds (optional)
- `DEFAULT_MOTION_STRENGTH`: Default motion strength (optional)
- `MAX_WAIT_TIME`: Maximum wait time for generation (optional)

### Video Settings

- **Resolutions**: 1280x768, 1920x1080, 768x1280, 1080x1920
- **Duration**: 1-10 seconds
- **Motion Strength**: 0.0-1.0 (controls amount of movement)

## Prompt Tips

### Best Practices

1. **Be specific and descriptive**
   - Good: "Close-up of morning dew on grass with soft golden sunlight"
   - Bad: "Nature scene"

2. **Include camera movements**
   - "Slow zoom into a flickering candle flame"
   - "Pan across a bustling city street at night"

3. **Mention lighting and mood**
   - "Cinematic lighting with dramatic shadows"
   - "Warm, cozy atmosphere with soft lighting"

4. **Add style references**
   - "In the style of a nature documentary"
   - "Cinematic shot with shallow depth of field"

### Example Prompts

- "A majestic eagle soaring over mountain peaks at golden hour"
- "Rain droplets falling on a window with blurred city lights in background"
- "Time-lapse of clouds moving across a blue sky"
- "Slow motion of waves crashing on a rocky shore"
- "Close-up of a hummingbird feeding from a red flower"

## API Reference

### RunwayTextToVideo Class

#### Methods

- `generate_video(text_prompt, duration, resolution, seed, motion_strength)`: Submit video generation request
- `check_generation_status(task_id)`: Check generation progress
- `wait_for_completion(task_id, max_wait_time)`: Wait for generation to complete
- `download_video(video_url, filename)`: Download generated video

#### Parameters

- `text_prompt` (str): Description of the video to generate
- `duration` (int): Video duration in seconds (1-10)
- `resolution` (str): Video resolution (see supported resolutions)
- `seed` (int, optional): Random seed for reproducibility
- `motion_strength` (float): Amount of motion (0.0-1.0)

## Error Handling

The client includes comprehensive error handling for:
- API rate limits
- Network timeouts
- Invalid parameters
- Generation failures
- Download errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Check the [Runway API documentation](https://docs.runwayml.com)
- Open an issue on GitHub
- Review the example prompts and configurations

## Changelog

### v1.0.0
- Initial release
- Web interface with Streamlit
- Command line interface
- Full API integration
- Configuration management
- Error handling and retry logic
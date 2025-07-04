import requests
import json
import time
import os
from typing import Optional, Dict, Any
import streamlit as st
from datetime import datetime

class RunwayTextToVideo:
    def __init__(self, api_key: str):
        """
        Initialize Runway API client
        
        Args:
            api_key: Your Runway API key
        """
        self.api_key = api_key
        self.base_url = "https://api.runwayml.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_video(self, 
                      text_prompt: str, 
                      duration: int = 4,
                      resolution: str = "1280x768",
                      seed: Optional[int] = None,
                      motion_strength: float = 0.8) -> Dict[str, Any]:
        """
        Generate video from text prompt
        
        Args:
            text_prompt: Description of the video to generate
            duration: Duration in seconds (1-10)
            resolution: Video resolution (1280x768, 1920x1080, etc.)
            seed: Random seed for reproducibility
            motion_strength: Amount of motion (0.0-1.0)
        
        Returns:
            Dictionary with generation task info
        """
        
        payload = {
            "text_prompt": text_prompt,
            "duration": duration,
            "resolution": resolution,
            "motion_strength": motion_strength
        }
        
        if seed:
            payload["seed"] = seed
        
        try:
            response = requests.post(
                f"{self.base_url}/generate",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"API Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
    
    def check_generation_status(self, task_id: str) -> Dict[str, Any]:
        """
        Check the status of a video generation task
        
        Args:
            task_id: The task ID returned from generate_video
        
        Returns:
            Dictionary with task status and video URL when complete
        """
        try:
            response = requests.get(
                f"{self.base_url}/tasks/{task_id}",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Status check failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Status check request failed: {str(e)}")
    
    def wait_for_completion(self, task_id: str, max_wait_time: int = 300) -> Dict[str, Any]:
        """
        Wait for video generation to complete
        
        Args:
            task_id: The task ID to monitor
            max_wait_time: Maximum time to wait in seconds
        
        Returns:
            Final task result with video URL
        """
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            try:
                result = self.check_generation_status(task_id)
                status = result.get("status", "")
                
                if status == "completed":
                    return result
                elif status == "failed":
                    raise Exception(f"Generation failed: {result.get('error', 'Unknown error')}")
                elif status in ["queued", "processing"]:
                    print(f"Status: {status}... waiting 10 seconds")
                    time.sleep(10)
                else:
                    print(f"Unknown status: {status}")
                    time.sleep(5)
                    
            except Exception as e:
                print(f"Error checking status: {str(e)}")
                time.sleep(5)
        
        raise Exception("Generation timed out")
    
    def download_video(self, video_url: str, filename: str) -> str:
        """
        Download generated video
        
        Args:
            video_url: URL of the generated video
            filename: Local filename to save video
        
        Returns:
            Path to downloaded video file
        """
        try:
            response = requests.get(video_url, stream=True, timeout=60)
            
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                return filename
            else:
                raise Exception(f"Download failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Download request failed: {str(e)}")

# Streamlit Web Interface
def create_streamlit_app():
    st.set_page_config(page_title="AI Text-to-Video Generator", page_icon="🎬")
    
    st.title("🎬 AI Text-to-Video Generator")
    st.subtitle("Create videos from text descriptions using Runway AI")
    
    # Sidebar for API key
    with st.sidebar:
        st.header("⚙️ Configuration")
        api_key = st.text_input("Runway API Key", type="password", 
                               help="Enter your Runway API key")
        
        if not api_key:
            st.warning("Please enter your Runway API key to continue")
            st.stop()
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Video Generation")
        
        # Text prompt input
        prompt = st.text_area(
            "Describe your video:",
            placeholder="A majestic eagle soaring over mountain peaks at sunset...",
            height=100
        )
        
        # Advanced options
        with st.expander("Advanced Options"):
            duration = st.slider("Duration (seconds)", 1, 10, 4)
            resolution = st.selectbox(
                "Resolution", 
                ["1280x768", "1920x1080", "768x1280", "1080x1920"]
            )
            motion_strength = st.slider("Motion Strength", 0.0, 1.0, 0.8, 0.1)
            seed = st.number_input("Seed (optional)", min_value=0, value=0)
            
        # Generate button
        if st.button("🎬 Generate Video", type="primary"):
            if not prompt.strip():
                st.error("Please enter a video description")
            else:
                generate_video_workflow(api_key, prompt, duration, resolution, motion_strength, seed)
    
    with col2:
        st.header("Tips for Better Results")
        st.markdown("""
        **🎯 Prompt Tips:**
        - Be specific and descriptive
        - Include camera movements
        - Mention lighting and mood
        - Keep it concise but detailed
        
        **📝 Examples:**
        - "A serene lake at dawn with mist rising"
        - "Close-up of raindrops on a window"
        - "Time-lapse of city traffic at night"
        - "Slow motion of a flower blooming"
        """)

def generate_video_workflow(api_key, prompt, duration, resolution, motion_strength, seed):
    """Handle the complete video generation workflow"""
    
    try:
        # Initialize client
        client = RunwayTextToVideo(api_key)
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Submit generation request
        status_text.text("🚀 Submitting generation request...")
        progress_bar.progress(10)
        
        result = client.generate_video(
            text_prompt=prompt,
            duration=duration,
            resolution=resolution,
            motion_strength=motion_strength,
            seed=seed if seed > 0 else None
        )
        
        task_id = result.get("id")
        if not task_id:
            st.error("Failed to start generation")
            return
        
        # Step 2: Monitor progress
        status_text.text("⏳ Generating video... This may take a few minutes")
        progress_bar.progress(30)
        
        # Wait for completion
        final_result = client.wait_for_completion(task_id)
        progress_bar.progress(80)
        
        # Step 3: Download and display
        video_url = final_result.get("video_url")
        if video_url:
            status_text.text("📥 Downloading video...")
            progress_bar.progress(90)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_video_{timestamp}.mp4"
            
            # Download video
            local_path = client.download_video(video_url, filename)
            progress_bar.progress(100)
            
            # Display results
            status_text.text("✅ Video generated successfully!")
            st.success("🎉 Your video is ready!")
            
            # Display video
            st.video(local_path)
            
            # Download button
            with open(local_path, "rb") as file:
                st.download_button(
                    label="📥 Download Video",
                    data=file.read(),
                    file_name=filename,
                    mime="video/mp4"
                )
            
            # Display generation info
            with st.expander("Generation Details"):
                st.json({
                    "prompt": prompt,
                    "duration": duration,
                    "resolution": resolution,
                    "motion_strength": motion_strength,
                    "task_id": task_id
                })
        
        else:
            st.error("Failed to generate video")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
        progress_bar.progress(0)
        status_text.text("")

# Command Line Interface
def create_cli_interface():
    """Simple command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate videos from text using Runway AI")
    parser.add_argument("--api-key", required=True, help="Runway API key")
    parser.add_argument("--prompt", required=True, help="Text description of video")
    parser.add_argument("--duration", type=int, default=4, help="Duration in seconds")
    parser.add_argument("--resolution", default="1280x768", help="Video resolution")
    parser.add_argument("--motion", type=float, default=0.8, help="Motion strength")
    parser.add_argument("--output", default="output.mp4", help="Output filename")
    
    args = parser.parse_args()
    
    # Generate video
    client = RunwayTextToVideo(args.api_key)
    
    print(f"Generating video: {args.prompt}")
    result = client.generate_video(
        text_prompt=args.prompt,
        duration=args.duration,
        resolution=args.resolution,
        motion_strength=args.motion
    )
    
    task_id = result.get("id")
    print(f"Task ID: {task_id}")
    
    # Wait for completion
    print("Waiting for generation to complete...")
    final_result = client.wait_for_completion(task_id)
    
    # Download video
    video_url = final_result.get("video_url")
    if video_url:
        print(f"Downloading video to {args.output}")
        client.download_video(video_url, args.output)
        print(f"Video saved: {args.output}")
    else:
        print("Generation failed")

if __name__ == "__main__":
    # Check if running in Streamlit
    try:
        import streamlit as st
        create_streamlit_app()
    except ImportError:
        print("Streamlit not installed. Running CLI version...")
        create_cli_interface()

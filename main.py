import yt_dlp
from moviepy.editor import AudioFileClip
import os
from tqdm import tqdm

def download_youtube_video_as_mp3(youtube_url, output_path=''):
    try:
        # Ensure output directory exists
        if output_path and not os.path.exists(output_path):
            os.makedirs(output_path)

        # Set up yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'progress_hooks': [progress_hook],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            base, _ = os.path.splitext(ydl.prepare_filename(info_dict))
            mp3_file = base + '.mp3'

        print(f"\nDownload and conversion complete: {mp3_file}")
        return mp3_file
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def progress_hook(d):
    if d['status'] == 'downloading':
        if 'downloaded_bytes' in d and 'total_bytes' in d:
            total_size = d['total_bytes']
            downloaded_size = d['downloaded_bytes']
            percentage = downloaded_size / total_size * 100
            pbar.update(downloaded_size - pbar.n)
            pbar.set_description(f"Downloading ({percentage:.2f}%)")
    elif d['status'] == 'finished':
        pbar.update(pbar.total - pbar.n)
        pbar.set_description("Download complete")
        pbar.close()

if __name__ == "__main__":
    url = input("Enter the YouTube URL: ")
    output_dir = input("Enter the output directory (leave blank for current directory): ").strip()
    
    # Initialize progress bar with unknown total size
    pbar = tqdm(total=100, unit='B', unit_scale=True, desc='Starting download', dynamic_ncols=True)

    # Start download
    download_youtube_video_as_mp3(url, output_dir)

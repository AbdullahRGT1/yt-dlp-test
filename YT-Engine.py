import yt_dlp
import os
import sys 
import time



print("YT-Engine.py loaded")

res_choice = ""  # Initialize res_choice variable



user_choice = {"url": "https://youtu.be/RVzs9B4qDvQ?si=tdlLOHfYxRqf2Neo", "res": res_choice}  # Get user input for video URL and desired resolution



save_path = "./downloads"  # Default save path

def get_video_info(video_url):
    info = yt_dlp.YoutubeDL().extract_info(video_url, download=False, extra_info=None)  # Extract video info :>
    filtered_info = {
        "title": info.get("title"),
        "duration": info.get("duration"),
        "formats": info.get("formats"),
    }


    return [filtered_info["title"],filtered_info["formats"]]



def process_formats(formats_list):
    """
    تستقبل قائمة الصيغ وتفلترها من صيغ الـ storyboard والحقول المكررة غير المهمة.
    """
    cleaned_formats = []
    
    for fmt in formats_list:
        # استبعاد صيغ الـ storyboard والملفات ذات الامتداد mhtml
        if fmt.get("format_note") == "storyboard" or fmt.get("ext") == "mhtml":
            continue
        
        # استبعاد العناصر التي لا تحتوي على صوت أو فيديو (تأكيد إضافي)
        if fmt.get("vcodec") == "none" and fmt.get("acodec") == "none":
            continue

        # استخراج البيانات الأساسية فقط
        cleaned_formats.append({
            "format_id": fmt.get("format_id"),
            "ext": fmt.get("ext"),
            "resolution": fmt.get("resolution") or f"{fmt.get('width', '')}x{fmt.get('height', '')}",
            "filesize_mb": round((fmt.get("filesize") or fmt.get("filesize_approx") or 0) / (1024 * 1024), 2),
            "vcodec": fmt.get("vcodec"),
            "acodec": fmt.get("acodec"),
            "fps": fmt.get("fps"),
            "tbr": fmt.get("tbr"),
            # "video_url": fmt.get("video_url")
        })
        
    return cleaned_formats


def organization(formats_list):
    unique_formats = {
        fmt["format_id"]: fmt
        for fmt in formats_list
        if fmt.get("format_id")
    }.values()

    sorted_formats = sorted(
        unique_formats,
        key=lambda x: x.get("tbr") or 0,
        reverse=True
    )

    return sorted_formats





def prepare_formats(formats_list):
    cleaned_formats = process_formats(formats_list)
    organized_formats = organization(cleaned_formats)

    return organized_formats







raw_formats = get_video_info(user_choice["url"])

organized_data = prepare_formats(raw_formats[1])


def resolution(video_res):
    Available_resolutions = []
    for i in video_res:
        if i["resolution"] is not None:
            Available_resolutions.append(i["resolution"]) if i["resolution"] not in Available_resolutions else None
    return Available_resolutions




# selecting res and storing in dictionary

print("\n\nTitle: ",raw_formats[0],"\n\n")  

print("Available Resolutions: ")  
 
 
counter = 1
for res in resolution(organized_data):
    print(f" {counter} - {res}")
    counter += 1

user_choice["res"] = resolution(organized_data)[int(input("\nSelect the resolution number: ")) - 1]  # Get user-selected resolution


print(user_choice)


    
    
    
    
    
    
def download_options(resolution, save_path):
    
       
    if "x" in str(resolution):
        res_number = resolution[resolution.index("x") + 1:]
    else:
        res_number = resolution  
        
    ydl_opts = {
        'format': f'best[height={res_number}]/bestvideo[height={res_number}]/best',
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'progress_hooks': [
            lambda d: print(f"Downloading: {d.get('filename', '')} - {d.get('_percent_str', '')} complete") if d.get('status') == 'downloading' else None
        ]
    }
    return ydl_opts

    



get_options = download_options(user_choice["res"], save_path)



with yt_dlp.YoutubeDL(get_options) as ydl:
         ydl.download([user_choice["url"]])

    
    
    
    

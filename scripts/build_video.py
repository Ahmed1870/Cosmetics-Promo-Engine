from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, ColorClip
import os

def process_video():
    # البحث عن ملف الفيديو تلقائياً
    video_path = None
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".mp4") and file != "final_promo.mp4":
                video_path = os.path.join(root, file)
                break

    print(f"Loading video from: {video_path}")
    base_video = VideoFileClip(video_path)
    w, h = base_video.size
    duration = base_video.duration

    # 1. تجهيز صورة العرض (products_group.jpg) مع حركة Zoom بطيئة
    try:
        products = ImageClip("assets/images/products_group.jpg")
        products = products.resize(width=w * 0.85).set_position('center')
        
        # ظهور تدريجي في الثانية 2 مع تكبير بنسبة 2% كل ثانية
        product_clip = (products
                        .set_start(2)
                        .set_duration(4)
                        .crossfadein(1)
                        .resize(lambda t: 1 + 0.02 * t))
    except Exception as e:
        print(f"Error loading products image: {e}")
        product_clip = None

    # 2. مشهد النهاية احترافي للوجو (logo.png)
    outro_duration = 3
    outro_bg = ColorClip(size=(w, h), color=(15, 15, 15)).set_duration(outro_duration)
    
    try:
        logo = ImageClip("assets/images/logo.png")
        logo_clip = (logo
                     .resize(width=w * 0.6)
                     .set_position('center')
                     .set_duration(outro_duration)
                     .crossfadein(1)
                     .resize(lambda t: 1 + 0.04 * t))
        
        outro_scene = CompositeVideoClip([outro_bg, logo_clip])
    except Exception as e:
        print(f"Error loading logo: {e}")
        outro_scene = outro_bg

    # 3. الدمج والتصدير
    if product_clip:
        main_comp = CompositeVideoClip([base_video, product_clip])
    else:
        main_comp = base_video

    final_video = CompositeVideoClip([
        main_comp.set_end(duration),
        outro_scene.set_start(duration - 1).crossfadein(1)
    ]).set_duration(duration + outro_duration - 1)

    final_video.write_videofile(
        "final_promo.mp4",
        fps=30,
        codec="libx264",
        audio_codec="aac",
        preset="fast",
        threads=4
    )

if __name__ == "__main__":
    process_video()
      

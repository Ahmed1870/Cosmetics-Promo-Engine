from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, ColorClip, vfx
import numpy as np
import os

def create_pulse_effect(t, duration):
    """تأثير نبض سينمائي خفيف يعطي حيوية للوجو"""
    return 1 + 0.03 * np.sin(2 * np.pi * t / duration)

def process_video():
    # البحث عن ملف الفيديو الاصلي
    video_path = None
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".mp4") and file != "final_promo.mp4":
                video_path = os.path.join(root, file)
                break

    print(f"--> Processing original video: {video_path}")
    base_video = VideoFileClip(video_path)
    w, h = base_video.size
    duration = base_video.duration

    # 1. إضافة صورة العرض مع تأثير Zoom In متدرج وطبقة ظلال أنيقة
    try:
        products = ImageClip("assets/images/products_group.jpg")
        # ضبط حجم الصورة لتناسب العرض
        prod_w = int(w * 0.75)
        products = products.resize(width=prod_w).set_position(('center', int(h * 0.15)))
        
        # ظهور في الثانية 1.5 ويستمر لـ 4.5 ثانية مع زوم ناعم وتلاشي
        product_clip = (products
                        .set_start(1.5)
                        .set_duration(4.5)
                        .crossfadein(0.8)
                        .crossfadeout(0.8)
                        .resize(lambda t: 1 + 0.015 * t))
    except Exception as e:
        print(f"Error loading products image: {e}")
        product_clip = None

    # 2. تصميم مشهد نهاية فخم للوجو (Cinematic Outro)
    outro_duration = 4
    # خلفية سوداء فاخرة
    outro_bg = ColorClip(size=(w, h), color=(10, 10, 12)).set_duration(outro_duration)
    
    try:
        logo = ImageClip("assets/images/logo.png")
        logo_w = int(w * 0.55)
        logo = logo.resize(width=logo_w).set_position('center')
        
        # تأثير نبض وتكبير تدريجي للوجو مع ظهور ناعم جداً
        logo_clip = (logo
                     .set_duration(outro_duration)
                     .crossfadein(1.2)
                     .resize(lambda t: (1 + 0.02 * t) * create_pulse_effect(t, outro_duration)))
        
        outro_scene = CompositeVideoClip([outro_bg, logo_clip])
    except Exception as e:
        print(f"Error loading logo: {e}")
        outro_scene = outro_bg

    # 3. دمج العناصر فوق الفيديو الرئيسي
    layers = [base_video]
    if product_clip:
        layers.append(product_clip)

    main_comp = CompositeVideoClip(layers)

    # 4. الربط مع مشهد النهاية وتطبيق Fade to Black
    final_video = CompositeVideoClip([
        main_comp.set_end(duration),
        outro_scene.set_start(duration - 1).crossfadein(1.2)
    ]).set_duration(duration + outro_duration - 1)

    # 5. التصدير بأعلى جودة ممكنة (Bitrate عالي للحفاظ على حجم الفيديو وصلابته)
    final_video.write_videofile(
        "final_promo.mp4",
        fps=30,
        codec="libx264",
        audio_codec="aac",
        bitrate="12000k",   # Bitrate مرتفع لضمان الوضوح التام والحفاظ على الجودة
        preset="veryslow",  # أعلى معالجة سينمائية ممكنة من FFmpeg
        threads=4
    )

if __name__ == "__main__":
    process_video()
    

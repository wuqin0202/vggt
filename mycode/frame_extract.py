import os
import cv2

def extract_frames(video_path, output_dir, interval_seconds=1.0):
    """
    从视频中按指定时间间隔抽取帧

    参数:
        video_path: 视频文件路径
        output_dir: 输出目录
        interval_seconds: 抽帧间隔(秒)，支持小数
    """
    os.makedirs(output_dir, exist_ok=True)

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"无法打开视频文件: {video_path}")

    # 获取视频属性
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    print(f"视频信息: {fps} FPS, 总帧数: {total_frames}, 时长: {duration:.2f}秒")

    frame_interval = fps * interval_seconds  # 转换为帧间隔
    accumulated_frames = 0.0  # 累计帧数（浮点数）
    saved_count = 0           # 已保存的帧数

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 当累计帧数超过间隔时保存当前帧
        if accumulated_frames >= frame_interval:
            output_path = os.path.join(output_dir, f"frame_{saved_count:06d}.png")
            cv2.imwrite(output_path, frame)
            saved_count += 1
            accumulated_frames -= frame_interval  # 减去已保存的间隔

        accumulated_frames += 1

    cap.release()
    print(f"抽帧完成，共保存 {saved_count} 帧")

# 测试用例
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="从视频中抽取帧")
    parser.add_argument("video_path", type=str, help="视频文件路径")
    parser.add_argument("output_dir", type=str, help="输出目录")
    parser.add_argument("--interval_seconds", "-i", type=float, default=1.0, help="抽帧间隔(秒)")
    args = parser.parse_args()
    extract_frames(args.video_path, args.output_dir, args.interval_seconds)
import requests
import time
import os

# 设置目标前缀
base_url = "https://moemiku.com/video/ios/"
headers = {"User-Agent": "Mozilla/5.0"}

# 设置起始和结束编号（
start_id = 1
end_id = 50  

# 是否保存结果
save_file = "found_videos.txt"
found = []

print(f"🚀 开始扫描 {base_url} 下的视频资源...\n")

for i in range(start_id, end_id + 1):
    filename = f"{i}.mp4"
    url = f"{base_url}{filename}"

    try:
        r = requests.head(url, headers=headers, timeout=1)  # 超时1秒
        if r.status_code == 200:
            print(f"✅ 找到视频: {url}")
            found.append(url)
        elif r.status_code == 403:
            print(f"🚫 被禁止访问: {url}")
        elif r.status_code != 404:
            print(f"⚠️ 状态 {r.status_code}: {url}")
    except Exception as e:
        print(f"❌ 请求出错: {url} — {e}")

    if i % 10 == 0:
        print(f"已扫描到第 {i} 个视频...")

    time.sleep(0.2)  # 延迟放在循环最后

# 写入结果文件
if found:
    with open(save_file, "w") as f:
        f.writelines(link + "\n" for link in found)
    print(f"\n📄 所有存在的视频已保存至：{save_file}")

    # 新增：下载视频
    download_dir = "downloaded_videos"
    os.makedirs(download_dir, exist_ok=True)
    print(f"\n⬇️ 开始下载视频到 {download_dir} 文件夹...")

    for url in found:
        filename = url.split("/")[-1]
        local_path = os.path.join(download_dir, filename)
        try:
            with requests.get(url, headers=headers, stream=True, timeout=10) as r:
                r.raise_for_status()
                with open(local_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            print(f"✅ 下载完成: {filename}")
        except Exception as e:
            print(f"❌ 下载失败: {filename} — {e}")

    print("🎉 所有可用视频下载完成！")
else:
    print("\n❗ 未发现任何可访问的视频。")

print("✅ 扫描结束。")
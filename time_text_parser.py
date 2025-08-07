import re
from datetime import datetime, timedelta

def parse_relative_time(text):
    if not isinstance(text, str):
        return datetime(2000, 1, 1, 0, 0, 0)

    now = datetime.now()

    # 去掉空格符 , . · 等符号
    text = text.replace(" ", "").replace("·", "")

    # 对应规则
    patterns = [
        (r"刚刚", lambda m: now),
        (r"(\d+)秒前", lambda m: now - timedelta(seconds=int(m.group(1)))),
        (r"(\d+)分钟前", lambda m: now - timedelta(minutes=int(m.group(1)))),
        (r"(\d+)小时前", lambda m: now - timedelta(hours=int(m.group(1)))),
        (r"昨天", lambda m: now - timedelta(days=1)),
        (r"(\d+)天前", lambda m: now - timedelta(days=int(m.group(1)))),
        (r"(一|1)周前", lambda m: now - timedelta(weeks=1)),
        (r"(半个月前)", lambda m: now - timedelta(days=15)),
        (r"(\d+)个月前", lambda m: now - timedelta(days=int(m.group(1)) * 30)),
    ]

    for pattern, handler in patterns:
        match = re.match(pattern, text)
        if match:
            dt = handler(match)
            return dt  # 如果你要时间戳就 return int(dt.timestamp())

    # 返回2000年1月1日 00:00:00
    return datetime(2000, 1, 1, 0, 0, 0)

if __name__ == "__main__":
    # 示例
    examples = ["刚刚", "30秒前", "5分钟前", "16小时前", "昨天", "3天前", "一周前", "半个月前", "2个月前", "· 5月24日"]

    for t in examples:
        dt = parse_relative_time(t)
        print(f"{t} -> {dt.strftime('%Y-%m-%d %H:%M:%S')} -> timestamp: {int(dt.timestamp())}")

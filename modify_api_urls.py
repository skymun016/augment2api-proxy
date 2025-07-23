#!/usr/bin/env python3
"""
修改Augment Token Manager插件的API地址
将远程API地址改为本地地址
"""

import base64
import os

def modify_class_file(file_path):
    """修改class文件中的API地址"""
    
    # 原始的Base64编码的API地址
    old_user_info_b64 = "aHR0cHM6Ly9hdWdtZW50LjE4NDc3Mi54eXovYXBpL3VzZXIvaW5mbw=="
    old_tokens_b64 = "aHR0cHM6Ly9hdWdtZW50LjE4NDc3Mi54eXovYXBpL3Rva2Vucw=="
    
    # 新的本地API地址
    new_user_info_url = "http://localhost:8787/api/user/info"
    new_tokens_url = "http://localhost:8787/api/tokens"
    
    # 编码为Base64
    new_user_info_b64 = base64.b64encode(new_user_info_url.encode()).decode()
    new_tokens_b64 = base64.b64encode(new_tokens_url.encode()).decode()
    
    print(f"原始 user/info API: {base64.b64decode(old_user_info_b64).decode()}")
    print(f"新的 user/info API: {new_user_info_url}")
    print(f"原始 tokens API: {base64.b64decode(old_tokens_b64).decode()}")
    print(f"新的 tokens API: {new_tokens_url}")
    print()
    print(f"原始 user/info Base64: {old_user_info_b64} (长度: {len(old_user_info_b64)})")
    print(f"新的 user/info Base64: {new_user_info_b64} (长度: {len(new_user_info_b64)})")
    print(f"原始 tokens Base64: {old_tokens_b64} (长度: {len(old_tokens_b64)})")
    print(f"新的 tokens Base64: {new_tokens_b64} (长度: {len(new_tokens_b64)})")
    print()
    
    # 读取文件
    with open(file_path, 'rb') as f:
        content = f.read()
    
    # 转换为字节串进行替换
    old_user_info_bytes = old_user_info_b64.encode('utf-8')
    old_tokens_bytes = old_tokens_b64.encode('utf-8')
    
    # 新的字节串需要填充到相同长度
    new_user_info_bytes = new_user_info_b64.encode('utf-8')
    new_tokens_bytes = new_tokens_b64.encode('utf-8')
    
    # 填充到相同长度（用空格填充）
    if len(new_user_info_bytes) < len(old_user_info_bytes):
        new_user_info_bytes += b' ' * (len(old_user_info_bytes) - len(new_user_info_bytes))
    
    if len(new_tokens_bytes) < len(old_tokens_bytes):
        new_tokens_bytes += b' ' * (len(old_tokens_bytes) - len(new_tokens_bytes))
    
    print(f"填充后的 user/info Base64: {new_user_info_bytes}")
    print(f"填充后的 tokens Base64: {new_tokens_bytes}")
    print()
    
    # 执行替换
    modified_content = content
    
    if old_user_info_bytes in content:
        modified_content = modified_content.replace(old_user_info_bytes, new_user_info_bytes)
        print("✅ 成功替换 user/info API地址")
    else:
        print("❌ 未找到 user/info API地址")
    
    if old_tokens_bytes in modified_content:
        modified_content = modified_content.replace(old_tokens_bytes, new_tokens_bytes)
        print("✅ 成功替换 tokens API地址")
    else:
        print("❌ 未找到 tokens API地址")
    
    # 写回文件
    with open(file_path, 'wb') as f:
        f.write(modified_content)
    
    print(f"\n✅ 文件修改完成: {file_path}")

if __name__ == "__main__":
    class_file = "com/augment/tokenmanager/plugin/util/StringProtector.class"
    
    if os.path.exists(class_file):
        modify_class_file(class_file)
    else:
        print(f"❌ 文件不存在: {class_file}")

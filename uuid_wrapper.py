import subprocess
import json
import sys
import os

# Add the Rust library path
rust_lib_path = r"d:\AI\lessmore\rust\utils"
sys.path.insert(0, rust_lib_path)

def call_uuid_function(func_name, *args):
    """
    调用Rust UUID库中的函数
    Call Rust UUID library functions
    """
    try:
        # 使用Python调用Rust函数
        # Use Python to call Rust functions
        if func_name == "generate_uuid1":
            # 生成UUID v1
            # Generate UUID v1
            result = subprocess.run(
                [sys.executable, "-c", f"""
import sys
sys.path.insert(0, r'{rust_lib_path}')
from uuid_utils import UUID
import uuid
# Generate UUID v1 using Rust library
node = {args[0]} if args[0] else None
clock_seq = {args[1]} if args[1] else None
print(uuid.uuid1(node, clock_seq))
"""],
                capture_output=True,
                text=True,
                timeout=30
            )
        elif func_name == "generate_uuid4":
            # 生成UUID v4
            # Generate UUID v4
            result = subprocess.run(
                [sys.executable, "-c", """
import sys
sys.path.insert(0, r'{}')
from uuid_utils import UUID
import uuid
print(uuid.uuid4())
""".format(rust_lib_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
        elif func_name == "generate_uuid5":
            # 生成UUID v5
            # Generate UUID v5
            namespace, name = args
            result = subprocess.run(
                [sys.executable, "-c", f"""
import sys
sys.path.insert(0, r'{rust_lib_path}')
from uuid_utils import UUID
import uuid
ns = UUID('{namespace}')
print(uuid.uuid5(ns.uuid, '{name}'))
"""],
                capture_output=True,
                text=True,
                timeout=30
            )
        else:
            return {"error": f"Unknown function: {func_name}"}
        
        if result.returncode == 0:
            return {"result": result.stdout.strip(), "status": "success"}
        else:
            return {"error": result.stderr, "status": "error"}
    except Exception as e:
        return {"error": str(e), "status": "error"}

def test_uuid_functions():
    """
    测试UUID函数
    Test UUID functions
    """
    print("Testing UUID functions...")
    
    # Test UUID v1
    print("\n1. Testing UUID v1 generation:")
    result = call_uuid_function("generate_uuid1", 12345, 67890)
    print(f"Result: {result}")
    
    # Test UUID v4
    print("\n2. Testing UUID v4 generation:")
    result = call_uuid_function("generate_uuid4")
    print(f"Result: {result}")
    
    # Test UUID v5
    print("\n3. Testing UUID v5 generation:")
    result = call_uuid_function("generate_uuid5", "6ba7b810-9dad-11d1-80b4-00c04fd430c8", "test-name")
    print(f"Result: {result}")

if __name__ == "__main__":
    test_uuid_functions()
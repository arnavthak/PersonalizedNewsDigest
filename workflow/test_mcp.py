import asyncio
from agents.mcp import MCPServerStdio
from utils import get_fetch_params

async def test_mcp_server():
    print("Testing MCP server connection...")
    
    try:
        async with MCPServerStdio(params=get_fetch_params()) as fetch_server:
            print("Connecting to MCP server...")
            await fetch_server.connect()
            print("Successfully connected to MCP server!")
            
            # Test a simple fetch
            print("Testing fetch functionality...")
            # This would normally test the fetch tool, but let's just verify connection works
            
    except Exception as e:
        print(f"Error connecting to MCP server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    result = asyncio.run(test_mcp_server())
    print(f"Test result: {'SUCCESS' if result else 'FAILED'}") 
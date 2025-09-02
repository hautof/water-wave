"""
Test script for weather functionality using the CLI
"""
import sys
import os
import subprocess
import json

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath('.'))

def test_weather_cli():
    """Test the weather functionality using the CLI"""
    print("Testing weather functionality using CLI...")
    
    # Change to the water-wave directory and activate the virtual environment
    os.chdir('/home/admin/workspace/water-wave')
    
    # Test running the CLI with a weather-related request
    try:
        # Run the CLI command to analyze a weather request
        result = subprocess.run(
            ['source venv/bin/activate && multi-agent-cli analyze "Get the weather forecast for Shanghai for the next 30 days" --format json'],
            shell=True,
            capture_output=True,
            text=True,
            executable='/bin/bash'
        )
        
        print("CLI command executed")
        print(f"Return code: {result.returncode}")
        print(f"Stdout: {result.stdout}")
        if result.stderr:
            print(f"Stderr: {result.stderr}")
            
        # Try to parse the output as JSON
        if result.stdout:
            try:
                output_data = json.loads(result.stdout)
                print("JSON output parsed successfully")
                print(f"Session ID: {output_data.get('session_id')}")
                print(f"Results: {output_data.get('results')}")
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON output: {e}")
        else:
            print("No output from CLI command")
                
    except Exception as e:
        print(f"Error during CLI execution: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_weather_cli()

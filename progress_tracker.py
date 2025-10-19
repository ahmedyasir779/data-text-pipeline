from tqdm import tqdm
import time
from typing import Iterable, Any


class ProgressTracker:
    @staticmethod
    def track(iterable: Iterable, description: str = "Processing", unit: str = "items") -> Iterable:
        """
        Track progress of an iterable
        
        Args:
            iterable: Items to iterate over
            description: Description to show
            unit: Unit name (items, files, rows, etc.)
            
        Returns:
            Wrapped iterable with progress bar
        """
        return tqdm(iterable, desc=description, unit=unit)
    
    @staticmethod
    def track_steps(total: int, description: str = "Processing") -> tqdm:
        """
        Create progress bar for manual steps
        
        Args:
            total: Total number of steps
            description: Description to show
            
        Returns:
            Progress bar object (call .update(1) to advance)
        """
        return tqdm(total=total, desc=description, unit="step")
    
    @staticmethod
    def track_operation(func, description: str = "Processing"):
        """
        Decorator to track operation time
        
        Args:
            func: Function to track
            description: Description to show
        """
        def wrapper(*args, **kwargs):
            print(f" {description}...")
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            print(f"✓ {description} complete ({elapsed:.2f}s)")
            return result
        return wrapper


# ============================================
# TESTING CODE
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("PROGRESS TRACKER - TEST")
    print("=" * 60)
    
    # Test 1: Track list processing
    print("\n1 Processing list with progress bar:")
    items = range(50)
    for item in ProgressTracker.track(items, "Processing items", "item"):
        time.sleep(0.02)  # Simulate work
    
    # Test 2: Manual step tracking
    print("\n2 Manual step tracking:")
    progress = ProgressTracker.track_steps(5, "Pipeline stages")
    
    time.sleep(0.3)
    progress.update(1)
    progress.set_description("Loading data")
    
    time.sleep(0.3)
    progress.update(1)
    progress.set_description("Cleaning")
    
    time.sleep(0.3)
    progress.update(1)
    progress.set_description("Analyzing")
    
    time.sleep(0.3)
    progress.update(1)
    progress.set_description("Visualizing")
    
    time.sleep(0.3)
    progress.update(1)
    progress.set_description("Complete")
    
    progress.close()
    
    # Test 3: Function decorator
    print("\n3 Function timing:")
    
    @ProgressTracker.track_operation
    def slow_function():
        time.sleep(0.5)
        return "Done"
    
    result = slow_function()
    
    print("\n" + "=" * 60)
    print("✓ TEST COMPLETE")
    print("=" * 60)
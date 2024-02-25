import logging
import time

from django.core.cache import cache


# ?metric_middleware
def metric_middleware(get_response):
    def middleware(request):
        # Get beginning stats
        start_time = time.perf_counter()

        # Process the request
        response = get_response(request)

        # Get ending stats
        end_time = time.perf_counter()

        # Calculate stats
        total_time = end_time - start_time

        # Log the results
        logger = logging.getLogger("debug")
        logger.info(f"Total time: {(total_time):.2f}s")
        print(f"Total time: {(total_time):.2f}s")

        print("Cached data is ", cache.get("pet_objects"))

        return response

    return middleware

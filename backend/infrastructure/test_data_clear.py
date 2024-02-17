import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


# ?TruncateTestData
def TruncateTestData(model):
    qs = model.objects.all()
    if qs is not None:
        for obj in qs:
            obj.pet_photo_url.delete()
            logging.info("Photo truncated successfully!")
    else:
        logging.error("Photo not truncated.Please try again!")

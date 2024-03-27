# def validate_post_photo(post_photo_url):
#     if not post_photo_url:
#         raise ValidationError(("Post photo is required."))
#     elif not post_photo_url.name.endswith((".png", ".jpg", ".jpeg")):
#         raise ValidationError(
#             ("Invalid file extension. Only PNG, JPG, and JPEG files are allowed.")
#         )

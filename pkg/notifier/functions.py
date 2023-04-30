def get_platform_profile(platform_name):
    if platform_name == "HackerOne":
        profile_url = "https://profile-photos.hackerone-user-content.com/variants/000/000/013/fa942b9b1cbf4faf37482bf68458e1195aab9c02_original.png/e60fe2d979b041d2254f8a36a3d2d7a24d7c4a8ad33ea024d13fc56668c7c4f6"
    elif platform_name == "Bugcrowd":
        profile_url = "https://logos.bugcrowdusercontent.com/logos/ef74/d1fa/62a5b64c/3809e0af42850a579f02c3434743e3ca_bugcrowd__1_.png"
    elif platform_name == "Intigriti":
        profile_url = "https://api.intigriti.com/file/api/file/public_bucket_d23a1f29-c2fe-4d03-8daf-df24d1e076ea-c2449aa2-3a08-4bf5-a430-441a11020851"
    elif platform_name == "YesWeHack":
        profile_url = "https://avatars.githubusercontent.com/u/16663829?s=280&v=4"
    return profile_url

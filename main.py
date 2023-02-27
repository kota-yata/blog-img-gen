from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

P_BLACK = "#333333"
P_ORANGE = "#C87F12"

ORIGINS = [
  "https://blog.kota-yata.com",
  "https://kota-yata.com",
  "https://blog-img-gen.an.r.appspot.com/"
  "http://localhost"
]
app.add_middleware(
  CORSMiddleware,
  allow_origins = ORIGINS,
  allow_methods = ["GET"]
)

fonts = {
  "nsjp": {
    "black": ImageFont.truetype("./static/fonts/NotoSansJP-Black.otf", 36),
    "medium": ImageFont.truetype("./static/fonts/NotoSansJP-Medium.otf", 24)
  },
  "inter": {
    "semi-bold": ImageFont.truetype("./static/fonts/Inter-SemiBold.ttf", 24)
  }
}

def generate_image(title, category, desc):
  img = Image.open("./static/ec.png")
  draw_obj = ImageDraw.Draw(img)
  draw_obj.text((100, 209), category, font = fonts["inter"]["semi-bold"], fill = P_ORANGE)
  draw_obj.text((100, 246), title, font = fonts["nsjp"]["black"], fill = P_BLACK)
  draw_obj.text((100, 333), desc, font = fonts["nsjp"]["medium"], fill = P_BLACK)
  return img

@app.get("/")
def root(title: str = "", category: str = "", desc: str = "", token: str = Depends(oauth2_scheme)):
  if token != os.getenv("BEARER_TOKEN"):
    raise HTTPException(
      status_code = 401,
      detail = "Invalid authentication credentials",
    )
  img = generate_image(title, category, desc)
  img_binary = BytesIO()
  img.save(img_binary, optimize = True, format = "PNG")
  response = Response(
    content = img_binary.getvalue(),
    status_code = 201,
    media_type = "image/png"
  )
  return response

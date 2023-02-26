from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from PIL import Image, ImageDraw, ImageFont
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
  "http://127.0.0.1/"
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
  img.save("./output.png", optimize = True, quality = 100)
  response = FileResponse(
    path = "./output.png",
    status_code = 201,
    media_type = "image/png"
  )
  return response

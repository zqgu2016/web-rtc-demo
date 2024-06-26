import os
from aiortc import (
    RTCPeerConnection,
    RTCSessionDescription,
)
from aiortc.contrib.media import MediaPlayer
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

ROOT = os.path.dirname(__file__)


class Offer(BaseModel):
    sdp: str
    type: str


class Answer(BaseModel):
    sdp: str
    type: str


@app.post("/api/offer")
async def create_offer(offer: Offer):
    offer = RTCSessionDescription(sdp=offer.sdp, type=offer.type)
    pc = RTCPeerConnection()
    videoPlayer = MediaPlayer(os.path.join(ROOT, "static/flower.mp4"))
    audioPlayer = MediaPlayer(os.path.join(ROOT, "static/demo-instruct.wav"))

    pc.addTrack(videoPlayer.video)
    pc.addTrack(audioPlayer.audio)


    # @pc.on("track")
    # def on_track(track):
    #     print("Track " + track.kind + " received")
    #     if track.kind == "video":
    #         pc.addTrack(videoPlayer.video)
    #     elif track.kind == "audio":
    #         pc.addTrack(audioPlayer.audio)

    await pc.setRemoteDescription(offer)

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return Answer(sdp=pc.localDescription.sdp, type=pc.localDescription.type)


app.mount("/", StaticFiles(directory="static", html=True), name="static")

const pc = new RTCPeerConnection();

pc.ontrack = (evt) => {
    const video = document.querySelector("video");
    if (evt.track.kind === "video") {
        video.srcObject = evt.streams[0];
        video.play();
    }
};

async function start() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: true,
        });
        stream.getTracks().forEach((track) => pc.addTrack(track, stream));
    } catch (err) {
        console.error("无法获取摄像头或音响设备: " + err);
    }

    negotiate()
};

async function negotiate() {
    await pc.setLocalDescription(await pc.createOffer());

    const res = await fetch("/api/offer", {
        method: "post",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            sdp: pc.localDescription.sdp,
            type: pc.localDescription.type,
        }),
    });
    const answer = await res.json();

    await pc.setRemoteDescription(answer);
}
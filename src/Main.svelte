<script lang="ts">
    import { onMount } from "svelte";

    let pc: RTCPeerConnection;

    onMount(async () => {
        pc = new RTCPeerConnection();

        let video = document.querySelector("video");

        pc.ontrack = (evt) => {
            if (evt.track.kind === "video") {
                video.srcObject = evt.streams[0];
                video.play();
            }
        };
    });

    const start = async () => {
        try {
            const videoOption = document.querySelector("[name=videoOption]:checked");
            const stream = await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: videoOption.value !== "videoOnly",
            });
            stream.getTracks().forEach((track) => pc.addTrack(track, stream));
        } catch (err) {
            console.error("无法获取摄像头或音响设备: " + err);
        }

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
    };
</script>

<div>
    <div class="container">
        <div class="video-option-item">
            <input type="radio" name="videoOption" value="all" checked />
            <label for="huey">播放视频和声音</label>
        </div>
        <div class="video-option-item">
            <input type="radio" name="videoOption" value="videoOnly" />
            <label for="huey">播放视频</label>
        </div>
        <button on:click={start}>Play</button>
    </div>

    <video controls width="250" height="250" />
</div>

<style>
    .container {
        display: flex;
        flex-direction: column;
        justify-content: start;
        align-items: start;
    }
    .video-option-item {
        display: flex;
        flex-direction: row;
        justify-content: start;
        align-items: center;
    }
</style>

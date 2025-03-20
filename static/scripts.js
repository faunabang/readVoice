document.addEventListener("DOMContentLoaded", () => {
    const initialDataAPI = "/api/get-initial-data";
    const streamAPI = "/stream";
    const timeline = document.getElementById("timeline");
    const processedTimestamps = new Set(); // 중복 방지를 위한 타임스탬프 기록

    // 초기 데이터 로드
    fetch(initialDataAPI)
        .then((response) => response.json())
        .then((data) => {
            data.forEach((item) => {
                // STT 텍스트가 비어있지 않고 중복되지 않은 항목만 추가
                if (item.stt_text && item.stt_text.trim() && !processedTimestamps.has(item.timestamp)) {
                    processedTimestamps.add(item.timestamp);
                    addToTimeline(item);
                }
            });

            // 초기 데이터 로드 완료 후 실시간 데이터 스트림 시작
            startSSE();
        })
        .catch((err) => {
            console.error("초기 데이터를 로드할 수 없습니다:", err);
        });

    // 실시간 데이터 스트림
    function startSSE() {
        const source = new EventSource(streamAPI);
        source.onmessage = (event) => {
            const newData = JSON.parse(event.data);
            // STT 텍스트가 비어있지 않고 중복되지 않은 항목만 추가
            if (newData.stt_text && newData.stt_text.trim() && !processedTimestamps.has(newData.timestamp)) {
                processedTimestamps.add(newData.timestamp);
                addToTimeline(newData);
            }
        };

        source.onerror = () => {
            console.error("SSE 연결 오류 발생");
        };
    }

    // 타임라인에 항목 추가
    function addToTimeline(item) {
        const timelineItem = document.createElement("div");
        timelineItem.classList.add("timeline-item");

        const time = document.createElement("div");
        time.classList.add("time");
        time.textContent = item.timestamp.split(" ")[1].slice(0, 5); // HH:mm 형식으로 표시

        const content = document.createElement("div");
        content.classList.add("content");

        const sttText = document.createElement("div");
        sttText.classList.add("stt-text");
        sttText.textContent = `STT: ${item.stt_text}`;

        const aiSummary = document.createElement("div");
        aiSummary.classList.add("ai-summary");
        aiSummary.textContent = `AI 요약: ${item.ai_summary}`;

        const playButton = document.createElement("button");
        playButton.classList.add("play-button");
        playButton.textContent = "▶";
        playButton.setAttribute("data-audio", item.audio_filename);
        playButton.addEventListener("click", () => {
            const audio = new Audio(item.audio_filename);
            audio.play().catch((error) => {
                console.error("Audio playback failed:", error);
            });
        });

        content.appendChild(sttText);
        content.appendChild(aiSummary);
        content.appendChild(playButton);

        timelineItem.appendChild(time);
        timelineItem.appendChild(content);

        timeline.prepend(timelineItem);
    }
});

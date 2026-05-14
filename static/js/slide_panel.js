document.addEventListener('DOMContentLoaded', function () {

    const getPanelAttribute = (attrs, panel, data) => {
        let itemDiv = document.createElement("div")
        itemDiv.classList.add("mb-4", "last:mb-0", "last:border-0", "border-b", "pb-3");

        Object.entries(attrs).forEach(([key, value]) => {
            if (!data[key]) return;

            let attrDiv = document.createElement("div");
            attrDiv.classList.add("mb-4", "last:mb-0", "flex", "flex-col", "justify-between");
            let keyDiv = document.createElement("div")
            keyDiv.classList.add("text-[0.8rem]", "font-medium", "text-muted")
            keyDiv.innerHTML = value
            attrDiv.appendChild(keyDiv)

            let valueDiv = document.createElement("div")
            valueDiv.classList.add("text-[1rem]", "whitespace-pre-wrap")
            if (key === "urls") {
                valueDiv.classList.add("mb-4", "last:mb-0", "pl-2");
                data[key].forEach(x => {
                    let anchor = document.createElement("a");
                    anchor.classList.add("hover:underline", "text-blue-600", "block")
                    anchor.href = x.url
                    anchor.innerHTML = x.keyword
                    valueDiv.appendChild(anchor)
                })
            } else if (typeof data[key] === "object") {
                valueDiv.classList.add("mb-4", "last:mb-0", "flex", "flex-row", "flex-wrap", "gap-2");
                data[key].map(x => x.name).forEach(x => {
                    let skillDiv = document.createElement("div");
                    skillDiv.classList.add("cstag", "bg-[#efefef]")
                    skillDiv.innerHTML = x
                    valueDiv.appendChild(skillDiv)
                })
            } else {
                valueDiv.innerHTML = data[key]
            }
            attrDiv.appendChild(valueDiv)
            itemDiv.appendChild(attrDiv)
        })
        panel.appendChild(itemDiv)
    }

    const getPanelBody = (attrs, panel, data, className = "") => {
        let itemDiv = document.createElement("div")
        itemDiv.classList.add("mb-4", "last:mb-0", "last:border-0", "border-b", "pb-3");
        if (className) itemDiv.classList.add(className)

        Object.entries(attrs).forEach(([key, value]) => {
            if (!data[key] || !data[key]?.length) return;
            let attrDiv = document.createElement("div");
            attrDiv.classList.add("mb-3", "last:mb-0", "last:mt-[1rem]", "flex", "flex-col", "justify-between");

            let keyDiv = document.createElement("div")
            let valueDiv = document.createElement("div")
            if (value.classnames?.length > 0) {
                valueDiv.classList.add(...value.classnames)
            } else {
                keyDiv.classList.add("text-[0.8rem]", "font-bold", "text-muted")
                keyDiv.innerHTML = value
                valueDiv.classList.add("text-[1rem]")
            }
            attrDiv.appendChild(keyDiv)

            if (data[key] === undefined) return;

            if (key === "skills") {
                valueDiv.classList.add("mb-4", "last:mb-0", "flex", "flex-row", "flex-wrap", "gap-2");
                data[key].map(x => x.name).forEach(x => {
                    let skillDiv = document.createElement("div");
                    skillDiv.classList.add("cstag", "bg-[#efefef]")
                    skillDiv.innerHTML = x
                    valueDiv.appendChild(skillDiv)
                })
            } else if (key === "files") {
                valueDiv.classList.add("mb-4", "last:mb-0", "flex", "flex-row", "flex-wrap", "gap-2");
                data[key].map(x => x.url).forEach(x => {
                    let fileAnchor = document.createElement("a");

                    let fileThumbnail = document.createElement("img");
                    fileThumbnail.classList.add("block", "project-files", "w-[120px]", "h-[120px]", "bg-cover", "bg-center", "rounded", "cursor-pointer")
                    fileThumbnail.src = x

                    fileAnchor.href = x
                    fileAnchor.appendChild(fileThumbnail)

                    valueDiv.appendChild(fileAnchor)
                })
            } else {
                valueDiv.innerHTML = data[key]
            }
            attrDiv.appendChild(valueDiv)
            itemDiv.appendChild(attrDiv)
        })
        panel.appendChild(itemDiv)
    }

    async function openPanel(dataId, dataType) {
        const panelTitle = document.getElementById('panel-title')
        const panelBody = document.getElementById("panel-body")

        panelTitle.innerHTML = `<div class="h-6 w-48 bg-gray-200 rounded animate-pulse"></div>`;
        panelBody.innerHTML = `<div class="flex flex-col gap-4 p-2">
            <div class="h-4 w-full bg-gray-200 rounded animate-pulse"></div>
            <div class="h-4 w-5/6 bg-gray-200 rounded animate-pulse"></div>
            <div class="h-4 w-4/6 bg-gray-200 rounded animate-pulse"></div>
            <div class="h-24 w-full bg-gray-200 rounded animate-pulse mt-2"></div>
            <div class="h-4 w-full bg-gray-200 rounded animate-pulse"></div>
            <div class="h-4 w-3/6 bg-gray-200 rounded animate-pulse"></div>
        </div>`;
        const data = await fetch(dataId).then(res => res.json())
        panelTitle.innerHTML = "";
        panelBody.innerHTML = "";

        if (dataType === "careers") {
            panelTitle.innerHTML = data.company;
            const attrs = {
                "introduction": "",
                "period": "재직 기간",
                "note": "참고 사항",
                "position": "직무 / 직급",
                "summary": "업무 요약",
                "skills": "기술스택",
            }
            getPanelAttribute(attrs, panelBody, data)

            data.projects.forEach(subData => {
                let bodies = {
                    "title": {classnames: ["font-bold", "text-xl"]},
                    "period": {classnames: ["text-muted"]},
                    "introduction": "",
                    "content": "주요 내용",
                    "result": "주요 성과",
                    "files": "참고 자료"
                }
                getPanelBody(bodies, panelBody, subData, "career-project-item")
            })
        } else if (dataType === "projects") {
            const attrs = {
                "introduction": "",
                "skills": "기술스택",
                "urls": "관련 링크",
            }
            getPanelAttribute(attrs, panelBody, data)
            panelTitle.innerHTML = data.title;
            let bodies = {
                "content": "주요 내용",
                "result": "주요 성과",
                "files": "참고 자료"
            }
            getPanelBody(bodies, panelBody, data)

        } else if (dataType === "skills") {
            panelTitle.innerHTML = data.name;
            const attrs = {
                "description": "",
            }
            getPanelBody(attrs, panelBody, data)
        }
        const panel = document.getElementById('slide-panel')
        panel.classList.remove('translate-x-full');
        panel.dataset.label = dataId
    }

    function closePanel() {
        const panel = document.getElementById('slide-panel')
        panel.classList.add('translate-x-full');
        delete panel.dataset.label;
    }

    document.addEventListener('click', async function (e) {
        const target = e.target.closest('.slide-panel');
        if (target) {
            const panel = document.getElementById('slide-panel')
            const dataId = target.dataset.id
            if (panel.dataset.label === dataId) {
                closePanel()
                return
            }

            const dataType = dataId.toString().split("/")[0]
            openPanel(dataId, dataType);
            return;
        }

        const slidePanel = e.target.closest('#slide-panel');
        const closePanelButton = e.target.closest('.close-panel');
        if (!slidePanel || closePanelButton) closePanel();
    })
})
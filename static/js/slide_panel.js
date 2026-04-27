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
            valueDiv.classList.add("text-[1rem]")
            if (typeof data[key] === "object") {
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
            attrDiv.classList.add("mb-3", "last:mb-0", "flex", "flex-col", "justify-between");

            let keyDiv = document.createElement("div")
            let valueDiv = document.createElement("div")
            if (value.classnames?.length > 0) {
                valueDiv.classList.add(...value.classnames)
            } else {
                keyDiv.classList.add("text-[0.8rem]", "font-bold")
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

    function openPanel(dataType, data) {
        const panelTitle = document.getElementById('panel-title')
        const panelBody = document.getElementById("panel-body")
        panelTitle.innerHTML = "";
        panelBody.innerHTML = "";

        if (dataType === "careers") {
            panelTitle.innerHTML = data.company;
            const attrs = {
                "introduction": "",
                "period": "재직 기간",
                "position": "직무 / 직급",
                "summary": "업무 요약",
                "skills": "기술스택",
            }
            getPanelAttribute(attrs, panelBody, data)

            data.projects.forEach(subData => {
                let bodies = {
                    "title": {classnames: ["font-bold", "text-xl"]},
                    "period": {classnames: ["text-muted"]},
                    "content": "주요 내용",
                    "result": "주요 성과",
                    "files": "참고 자료"
                }
                getPanelBody(bodies, panelBody, subData, "career-project-item")
            })
        } else if (dataType === "projects") {
            panelTitle.innerHTML = data.title;
            const attrs = {
                "introduction": "",
                "skills": "기술스택",
            }
            getPanelAttribute(attrs, panelBody, data)

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
            getPanelAttribute(attrs, panelBody, data)
        }

        document.getElementById('slide-panel').classList.remove('translate-x-full', "hidden");
    }

    function closePanel() {
        document.getElementById('slide-panel').classList.add('translate-x-full', "hidden");
        document.getElementById('main-content').style.marginRight = '0';
    }

    document.addEventListener('click', async function (e) {
        const target = e.target.closest('.slide-panel');
        if (target) {
            e.preventDefault()
            const dataType = target.dataset.id.toString().split("/")[0]
            const response = await fetch(target.dataset.id).then(res => res.json())
            openPanel(dataType, response);
            return;
        }

        const slidePanel = e.target.closest('#slide-panel');
        const closePanelButton = e.target.closest('.close-panel');
        if (!slidePanel || closePanelButton) closePanel();
    })
})
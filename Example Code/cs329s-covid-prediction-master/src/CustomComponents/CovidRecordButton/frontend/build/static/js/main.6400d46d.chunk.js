(this.webpackJsonpstreamlit_component_template=this.webpackJsonpstreamlit_component_template||[]).push([[0],{7:function(e,t,a){e.exports=a(8)},8:function(e,t,a){"use strict";a.r(t);var n=a(3),r=a(6);window.MediaRecorder=r.a;var o=document.body.appendChild(document.createElement("span")).appendChild(document.createElement("button"));o.classList.add("covid-button"),o.textContent="Start Recording";var i=null,d=5e3,s=null;function c(){i.stop(),o.textContent="Start Recording",i.stream.getTracks().forEach((function(e){return e.stop()}))}o.onclick=function(){navigator.mediaDevices.getUserMedia({audio:!0}).then((function(e){(i=new MediaRecorder(e)).addEventListener("dataavailable",(function(e){var t,a=new FileReader;a.onload=function(a){t=new Uint8Array(a.target.result),t=Array.from(t);var r=URL.createObjectURL(e.data);n.a.setComponentValue(JSON.stringify({data:t,url:r}))},a.readAsArrayBuffer(e.data)})),null!==s&&clearTimeout(s),i.start(),o.textContent="Restart Recording",n.a.setComponentValue("clicked"),s=setTimeout(c,d)}))},n.a.events.addEventListener(n.a.RENDER_EVENT,(function(e){var t=e.detail;o.disabled=t.disabled,d=t.args.duration,n.a.setFrameHeight()})),n.a.setComponentReady(),n.a.setFrameHeight()}},[[7,1,2]]]);
//# sourceMappingURL=main.6400d46d.chunk.js.map
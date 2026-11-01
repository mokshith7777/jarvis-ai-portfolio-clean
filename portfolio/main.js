(() => {
 const canvas=document.getElementById('webgl'); if(!canvas)return;
 const gl=canvas.getContext('webgl2',{alpha:true,antialias:false,powerPreference:'low-power'});
 if(!gl){canvas.style.display='none';return;}
 const vertex=`#version 300 es
 in vec2 position; out vec2 uv; void main(){uv=position*.5+.5;gl_Position=vec4(position,0.,1.);}`;
 const fragment=`#version 300 es
 precision highp float; in vec2 uv; out vec4 color; uniform vec2 resolution; uniform float time;
 float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
 void main(){vec2 p=(uv-.5)*vec2(resolution.x/resolution.y,1.);float r=length(p);float a=atan(p.y,p.x);float grid=abs(sin(a*24.+r*35.+time*.12));float ring=smoothstep(.012,0.,abs(r-(.28+.018*sin(a*5.+time*.25))));float rays=smoothstep(.96,1.,grid)*smoothstep(.8,.15,r);float glow=exp(-r*3.2)*.12;vec3 cyan=vec3(0.,.65,.8);vec3 red=vec3(.8,0.,.12);vec3 c=mix(cyan,red,.5+.5*sin(a*2.+time*.12));float v=ring*.55+rays*.12+glow;color=vec4(c*v,v*.8);}`;
 function shader(type,src){const s=gl.createShader(type);gl.shaderSource(s,src);gl.compileShader(s);return gl.getShaderParameter(s,gl.COMPILE_STATUS)?s:null;}
 const vs=shader(gl.VERTEX_SHADER,vertex),fs=shader(gl.FRAGMENT_SHADER,fragment);if(!vs||!fs){canvas.style.display='none';return;}
 const program=gl.createProgram();gl.attachShader(program,vs);gl.attachShader(program,fs);gl.linkProgram(program);if(!gl.getProgramParameter(program,gl.LINK_STATUS)){canvas.style.display='none';return;}
 const buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),gl.STATIC_DRAW);
 const loc=gl.getAttribLocation(program,'position');gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,2,gl.FLOAT,false,0,0);
 const resolution=gl.getUniformLocation(program,'resolution'),time=gl.getUniformLocation(program,'time');
 let width=0,height=0,raf=0,start=performance.now(),visible=true,contextLost=false;
 function resize(){const dpr=Math.min(devicePixelRatio||1,1.5),w=Math.floor(innerWidth*dpr),h=Math.floor(innerHeight*dpr);if(w!==width||h!==height){width=w;height=h;canvas.width=w;canvas.height=h;gl.viewport(0,0,w,h);}}
 function draw(now){if(!visible||contextLost)return;resize();gl.clearColor(0,0,0,0);gl.clear(gl.COLOR_BUFFER_BIT);gl.useProgram(program);gl.uniform2f(resolution,width,height);gl.uniform1f(time,(now-start)/1000);gl.drawArrays(gl.TRIANGLE_STRIP,0,4);raf=requestAnimationFrame(draw);}
 const observer=new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;if(visible&&!contextLost){cancelAnimationFrame(raf);raf=requestAnimationFrame(draw)}else cancelAnimationFrame(raf)});observer.observe(canvas);
 document.addEventListener('visibilitychange',()=>{visible=!document.hidden;if(visible&&!contextLost)raf=requestAnimationFrame(draw);else cancelAnimationFrame(raf)});
 canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();contextLost=true;cancelAnimationFrame(raf)});
 canvas.addEventListener('webglcontextrestored',()=>{contextLost=false;start=performance.now();raf=requestAnimationFrame(draw)});
 addEventListener('resize',resize,{passive:true});raf=requestAnimationFrame(draw);
 const glow=document.querySelector('.cursor-glow');if(matchMedia('(pointer:fine)').matches){addEventListener('pointermove',e=>{glow.style.left=e.clientX+'px';glow.style.top=e.clientY+'px'},{passive:true})}else glow.style.display='none';
 const menu=document.querySelector('.menu');menu?.addEventListener('click',()=>{const nav=document.querySelector('nav');const open=nav.dataset.open==='1';nav.dataset.open=open?'0':'1';Object.assign(nav.style,{display:open?'none':'flex',position:'absolute',top:'68px',left:'0',right:'0',padding:'24px 7vw',background:'#080a0e',flexDirection:'column',gap:'22px',borderBottom:'1px solid #ffffff22'})});
})();
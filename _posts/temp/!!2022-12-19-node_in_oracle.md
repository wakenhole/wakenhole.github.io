---
title: "Node js in Oracle cloud"
categories: [Tech, Cloud & Ops]
tags:
  - Optimization
  - C++
  - vector
  - Programming
toc: true
toc_sticky: true
tagline: "C++"
image:
  overlay_image: https://images.unsplash.com/photo-1625459201773-9b2386f53ca2?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1630&q=80
  overlay_filter: 0.5
  caption: "[**Unsplash**](https://unsplash.com)"
  path: https://images.unsplash.com/photo-1550439062-609e1531270e?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80
---

> Add user
```
sudo adduser username
usermod -aG sudo username
mkdir /home/username/.ssh
sudo cp /home/ubuntu/.ssh/authorized_keys /home/username/.ssh
```


> Update node
```bash
sudo apt update
sudo apt install npm net-tools
sudo npm cache clean --force
sudo npm install -g n
sudo n stable
node --version
```

> Update npm
```bash
sudo npm install -g npm http-server nohup yarn
npm install --save @types/d3-shape
```

```bash
sudo ufw allow 80
sudo ufw allow 443
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo netfilter-persistent save
sudo nohup http-server -p 80
sudo  http-server -p 80
```

https://wormwlrm.github.io/2021/11/07/Rollup-React-TypeScript.html

https://bohyeon-n.github.io/deploy/front-end/rollup.html


```bash
# 전역 설치
yarn global add rollup

# 프로젝트 의존성으로 설치
yarn add -D rollup
npm install --save-dev rollup-plugin-node-resolve
```


```json
// package.json

{
  "devDependencies": {
    "rollup": "^3.7.5"
  },
  "scripts": {
    "build": "rollup -c",
    "watch": "rollup -cw"
  },
  "main": "./dist/bundle.js",
  "type": "module"
}

```

```json
// rollup.config.js

export default {
    input: "./src/index.js", // 진입 경로
    output: {
      file: "./src/bundle.js", // 출력 경로
      format: "cjs", // 출력 형식
      sourcemap: true, // 소스 맵을 켜놔서 디버깅을 쉽게 만들자
    },
  };
```


```bash
# NPM 스크립트
yarn build

# 그냥 롤업에서 바로
rollup -c

# NPM 스크립트
yarn watch

# 그냥 롤업에서 바로
rollup -cw
```

```bash
# 피어 디펜던시로 설치
yarn add -P react react-dom
yarn add -D @babel/core @babel/preset-env @babel/preset-react
yarn add -D @rollup/plugin-babel 
yarn add @types/d3-shape

```

```json
// rollup.config.js

import babel from "@rollup/plugin-babel";


export default {
    input: "./src/index.js", // 진입 경로
    output: {
      file: "./src/bundle.js", // 출력 경로
      format: "cjs", // 출력 형식
      sourcemap: true, // 소스 맵을 켜놔서 디버깅을 쉽게 만들자
    },
  plugins: [
    // 바벨 트랜스파일러 설정
    babel({
      babelHelpers: "bundled",
      presets: ["@babel/preset-env", "@babel/preset-react"],
    }),
  ],
  };
```
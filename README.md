# Video Compressor Service

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![NPM](https://img.shields.io/badge/NPM-%23CB3837.svg?style=for-the-badge&logo=npm&logoColor=white)
![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![React Router](https://img.shields.io/badge/React_Router-CA4245?style=for-the-badge&logo=react-router&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white)

動画圧縮を行うウェブアプリケーション

## Usage Examples (Demo)

Comming Soon...

## Description

このサービスは、動画圧縮サービスです。

このサービスは、動画からオーディオや GIF など異なるフォーマットを作成したり解像度を変換する場面の使用を考えています。

ユーザは圧縮や解像度変更、フォーマットコンバージョンを行いたい動画ファイルを選択します。

その後、サービスをブラウザから選択すると圧縮等がなされたファイルをダウンロードすることができます。

基本的な機能として、下記のような機能を提供しています。

- 動画ファイルを圧縮する(圧縮の度合いを low, medium, high から選択できます)

- 動画の解像度を変更する

- 動画の縦横比を変更する

- 動画をオーディオに変換する

- 指定した時間範囲から GIF を作成する

詳細は Usage Example をご覧になってください。

## Requirements

このプロジェクトをローカル環境で動かすためには**Python 3.X**と**Node.Js**、**npm**, **ffmpeg**が必要です。

```zsh
% ffmpeg -version
ffmpeg version 6.1.1 Copyright (c) 2000-2023 the FFmpeg developers
```

上記のような実行結果であれば大丈夫です。ffmpeg は version 6.1.1 では動作することを確認済みです。

これらが揃っている場合いかに進んでください。

## Getting Started (Installation)

```zsh
% git clone git@github.com:TlexCypher/VideoCompressor.git
% cd VideoCompressor
% cd backend
% cd socket
% cd server
% python3 vc_server.py # backendのサーバー側を起動
% cd ../client/api
% python3 routes.py # backendのクライアント側を起動
% cd ../frontend
% npm install
% npm run dev # fronendを起動
```

## Why I made this app?

今まで構築してきた Web アプリケーションは、単純な HTTP 通信を使ったクライアントサーバモデルを採用してきました。

しかし、最近 OSI 参照モデルなどについて勉強したこともあり、アプリケーション層とトランスポート層という違うレイヤーのプロトコルを 1 つのアプリケーションで使う機会を経験したいと思い、挑戦に至りました。

また、卒論や README の執筆時など動画を圧縮したいと思う機会が刹那的ではあるが重なったため、自分で作る挑戦をしました。

## System Design


<img width="963" alt="SystemDesignCompman" src="https://github.com/TlexCypher/VideoCompressor/assets/144787772/2ec857b7-360c-4641-af19-45edc4809944">



## Functionalities wanna to add in the future

- サービスがどのくらい終了しているかがわかるプログレスバーを表示したい

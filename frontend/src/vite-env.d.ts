/// <reference types="vite/client" />

declare module 'hls.js' {
  export default class Hls {
    static isSupported(): boolean;
    constructor(config?: any);
    loadSource(url: string): void;
    attachMedia(video: HTMLVideoElement): void;
    on(event: string, callback: Function): void;
    destroy(): void;
  }
}

// preload.js

const { contextBridge, ipcRenderer } = require('electron');

//window.ipcRenderer = ipcRenderer;
contextBridge.exposeInMainWorld('electronAPI', {
    setTitle: (val) => ipcRenderer.send('sendMessageToMainProcess', val)
  })
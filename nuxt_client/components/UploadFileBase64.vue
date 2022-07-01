<template>
  <div>
    <!-- limit input file type here -->
    <v-file-input v-model="file" accept="image/*" show-size @change="onChangeFileInput">
    </v-file-input>
    <v-btn @click.stop="onClickUploadFile">submit</v-btn>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
interface Data {
  file: File | null;
  dataBase64: string;
}
export default Vue.extend({
  name: "UploadFile_base64",
  props: {
    value: {
      type: String,
      default: null,
    },
  },
  data(): Data {
    return {
      file: null,
      dataBase64: "",
    };
  },
  methods: {
    onChangeFileInput(): void {
      if(this.file === null){
        return;
      }
      const reader: FileReader = new FileReader();
      reader.onload = (event) => {
        if (reader.result !== null) {
          if (typeof reader.result === "string") {
            const offset: number = reader.result.indexOf(",") + 1;
            this.dataBase64 = reader.result.slice(offset);
          }
        }
      };
      reader.readAsDataURL(this.file);
    },
    async onClickUploadFile(): Promise<void> {
      if(this.file === null){
        return;
      }
      const url: string = "http://127.0.0.1:3001/rtnfile64";
      const send_data: {contentData: string, fileName: string} = {
        contentData: this.dataBase64,
        fileName: this.file.name,
      };
      const res: Response = await fetch(url, {
        method: "POST",
        mode: "cors",
        body: JSON.stringify(send_data),
        headers: {
          "Content-Type": "application/json",
        },
      });
      if (!res.ok) {
        console.log(`${res.status} ${res.statusText}`);
        throw new Error(`${res.status} ${res.statusText}`);
      }
      // Get file url
      const resJson: {contentData: string, fileName: string} = await res.json();
      const base64Blob: Blob = await this.base64DecodeAsBlob(resJson["contentData"])
      const objUrl: string = window.URL.createObjectURL(base64Blob);
      // Get file name
      const header: string | null = res.headers.get('Content-Disposition');
      let filename: string = "";
      if (header !== null) {
        const parts = header!.split(';');
        filename = parts[1].split('=')[1].replace(/\"/g, "");
      } else {
        filename = "downloadFile"
      }
      // Download File
      const a: HTMLAnchorElement = document.createElement("a");
      a.href = objUrl;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(objUrl)
    },
    async base64DecodeAsBlob(text: string, type: string = "text/plain;charset=UTF-8"): Promise<Blob> {
      return fetch(`data:${type};base64,` + text).then((response) => response.blob());
    },
  },
});
</script>

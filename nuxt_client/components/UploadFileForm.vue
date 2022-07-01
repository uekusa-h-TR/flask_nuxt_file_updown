<template>
  <div>
    <!-- limit input file type here -->
    <v-file-input v-model="file" accept="image/*" show-size> </v-file-input>
    <v-btn @click.stop="onClickUploadFile">submit</v-btn>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
interface Data{
  file: File | null
}
export default Vue.extend({
  name: "UploadFile",
  props: {
    value: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      file: null,
    };
  },
  methods: {
    async onClickUploadFile(): Promise<void> {
      if(this.file === null){
        return;
      }
      const url: string = "http://127.0.0.1:3001/rtnfile";
      const formData: FormData = new FormData();
      formData.append("file", this.file!);
      const res: Response = await fetch(url, {
        method: "POST",
        mode: "cors",
        body: formData,
      })
      if (!res.ok) {
        console.log(`${res.status} ${res.statusText}`);
        throw new Error(`${res.status} ${res.statusText}`);
      }
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
      const objUrl: string = window.URL.createObjectURL(await res.blob());
      const a: HTMLAnchorElement = document.createElement("a");
      a.href = objUrl;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(objUrl)
    },
  },
});
</script>

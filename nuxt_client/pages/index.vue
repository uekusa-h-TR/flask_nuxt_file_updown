<template>
  <div>
    <h1>{{title}}</h1>

    <UploadFileForm/>
    <UploadFileBase64/>
  </div>
</template>

<script>
import UploadFileForm from '~/components/UploadFileForm.vue'
import UploadFileBase64 from '~/components/UploadFileBase64.vue'
export default {
  name: 'IndexPage',
  data: ()=>({
    title: "File Upload and Download",
    titleUploadForm: "Upload image by form data",
    titleUploadBase64: "upload image by json base64",
  }),
  components:{
    UploadFileForm,
    UploadFileBase64
  }
}
</script>

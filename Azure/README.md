# Azure 
The azure pipelines can be created from the templates. Change the following items in the pipeline to make it work with your Azure Devops
- trigger : none or the branch or branches as list. A push trigger specifies which branches cause a continuous integration build to run.
- pool -> name: the agent pool you want to use for the build, this should match the agent which is installed with ArcGIS Server or ArcGIS Pro
- script: update the directories for the ArcGIS Server Python, the GaiaBuilder Directory , the file you want to deploy and the environment it should be deployed to
- env -> USER: the Portal build-in user you want to use for authentication in the build
- env -> PASSWORD: the password variable as secret configured on your pipeline, store the password as a secret in the pipeline to avoid storing the password in the repository.



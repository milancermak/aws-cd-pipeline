# aws-cd-pipeline
A demo project of a CD pipeline built with AWS Code-suite tools for a talk I gave. [Slides are available on Speakerdeck](https://speakerdeck.com/milancermak/cd-pipeline-on-aws).

### Start
To get up and running, clone the repo and create the pipeline in your AWS account:
```sh
REGION=eu-central-1
SERVICE_NAME=cd-demo
STACK_NAME=cd-demo-pipeline

aws cloudformation create-stack \
--region ${REGION} \
--stack-name ${STACK_NAME} \
--template-body file://infrastructure/pipeline.yml \
--parameters ParameterKey=Service,ParameterValue=${SERVICE_NAME} \
--tags Key=Service,Value=${SERVICE_NAME} \
--capabilities CAPABILITY_IAM
```

Wait until the stack is created. Then, get the git URL of the CodeCommit repo:
```sh
aws cloudformation describe-stacks \
--region ${REGION} \
--stack-name ${STACK_NAME} \
--query 'Stacks[0].Outputs'
```
Add it as a new remote:
```sh
# replace the URL
git remote add aws ssh://git-codecommit.eu-central-1.amazonaws.com/v1/repos/cd-demo
```
And finally push to that repository `git push aws master`. That should trigger the first run of the pipeline.

### Tips, tricks, opinions, dos and donts
Here's an assorted and opinionated list of things to consider when creating a CD pipeline. Some you can apply right away, some are more advanced which you can build in later iterations.

* **Always** make the pipeline update itself as the second stage. This is very easy to do, just copy the second stage in this example pipeline. Don't forget to set the [`RestartExecutionOnUpdate`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-restartexecutiononupdate) to `true`.
* Always pass **all** the template parameters back via the `ParameterOverrides`. This is 1) easy to forget and 2) error-prone as you need to write a JSON string with CloudFormation string interpolation syntax inside a YAML 🤷‍♂️.
* Automate everything.
* Consider measuring the following metrics:
  * Execution duration of the whole pipeline
  * Execution duration of the build process (CodeBuild)
  * Execution fail rate
* Prefer GitHub instead of CodeCommit because it's region agnostic and slightly faster to trigger the pipeline execution.
* Be careful if using SAM for deployments (the `AutoPublishAlias` and `DeploymentPreference` combo). It can work well, but it's too much magic.
* Be **absolutely sure** the CloudWatch alarm you use to monitor a successful/failed deployment triggers correctly.
* When deploying across multiple regions, start in a low traffic one.
* Don't use a gradual rollout policy for non-production stages.
* Have separate, isolated deployment stages and resources as much as possible (e.g. dev, alpha, beta, qa, prod, ...).
* Have separate, isolated AWS accounts per deployment stage.
* CodeBuild tips:
  * Run verbose commands in quite mode
  * Print useful progress messages
  * Use a cache to speed up your build
  * Put "complex" multiline commands in a `.sh` file. 
  * Update the aws-cli if you need support for newish services
  * Use [CodeBuild local](https://github.com/aws/aws-codebuild-docker-images/tree/master/local_builds) for debugging

### Documentation links
The official documentation is pretty great, but hard to navigate. Here's a list of starting points that will hopefully help you to find what you're looking for.

* [CodePipeline Action structure](https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html#action-requirements)
* [CodePipeline Stage Action property in CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions.html)
* [CodePipeline data types](https://docs.aws.amazon.com/codepipeline/latest/APIReference/API_Types.html)
* [Using Fn::GetArtifactAtt & Fn::GetParam with ParameterOverrides](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-parameter-override-functions.html)
* [CloudFormation configuration properties](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-action-reference.html#w2ab1c13c13b9)
* [CloudFormation artifacts](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html)

### Other helpful presentations
* [Sarah Wells from Financial Times, QCon London 2019](https://speakerdeck.com/sarahjwells/qcon-london-2019-mature-microservices-and-how-to-operate-them) - especially the first third on why you really want to have a CD pipeline
* [Serverless workflows for the enterprise](https://www.youtube.com/watch?v=T4RWwD5oHUc) (get the slides [here](https://pages.awscloud.com/Serverless-Workflows-for-the-Enterprise_1107-SRV_OD.html) by filling out the stupid form). Good overview of some advanced techniques.

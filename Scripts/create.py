from email.mime import base
from botocore.exceptions import ClientError
import boto3, glob, os, shutil
from zipfile import ZipFile
 
sourcedir = '/Users/sbdishman/Dropbox/repo/github_sbdishman/aws-securityapp/lambda'
bucketname = 'securityapp-lambda-source'
my_access_key_id = 'putSomethingHere'
my_secret_access_key = 'putSomethingHere'
my_region_name = 'us-east-1'
my_role_arn = 'putSomethingHere'
destfilename = "lambda_function.py"
 
if os.path.isdir(sourcedir):
    os.chdir(sourcedir)
    if os.path.isfile(destfilename):
        os.remove(destfilename)
    worklist = glob.glob('*.py')
    worklist.sort()
    for workitem in worklist:
        basename = workitem[0:-3]
        basezipname = basename + ".zip"
        fullzipname = sourcedir + "/" + basezipname
        sourcefilename = sourcedir + "/" + workitem
        print()
        print("Publishing lambda function: {}".format(basename))
 
        #
        ## Cleaning up and setting up
        #
        if os.path.isfile(fullzipname):
            print("      Zip file {} exists. Removing it.".format(fullzipname))
            os.remove(fullzipname)
        print("      Creating function file: {}/lambda_function.py".format(basename))
        shutil.copy(sourcefilename,destfilename)    
 
        #
        ## Create zip file
        #
        print("      Creating zip file.")
        with ZipFile(fullzipname,'w') as myzip:
            myzip.write("lambda_function.py")
        myzip.close()
 
        #
        ## Push to s3
        #
        session = boto3.Session(aws_access_key_id = my_access_key_id, aws_secret_access_key = my_secret_access_key, region_name = my_region_name)
        s3 = session.resource('s3')
        mybucket = s3.Bucket(bucketname)
        for myfile in mybucket.objects.all():
            if myfile.key == basezipname:
                print("      Removing existing file from s3")
                s = boto3.client('s3',aws_access_key_id = my_access_key_id, aws_secret_access_key = my_secret_access_key)
                s.delete_object(Bucket=bucketname,Key=myfile.key)
        print("      Adding file to s3")
        mybucket.upload_file(fullzipname,basezipname)
 
        print("      Updating function code")
        l = session.client('lambda')
        try:
            l.update_function_code(
                FunctionName=basename,
                S3Bucket=bucketname,
                S3Key=basezipname
            )
        except ClientError as e:
            if e.response['Error']['Code'] == "ResourceNotFoundException":
                print("      Lambda function not found. Creating function.")
                l.create_function(
                    FunctionName = basename,
                    Runtime = 'python3.9',
                    Role = my_role_arn,
                    Handler = basename + ".lambda_handler",
                    Code = {
                        'S3Bucket' : bucketname,
                        'S3Key' : basezipname
                    }
                )

        #
        ## Clean up
        #
        print("      Cleaning up.")
        os.remove(fullzipname)
        os.remove(destfilename)
else:
    print("ERROR: Missing source directory")
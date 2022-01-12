import numpy as np
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import pickle
from tqdm import tqdm

# in 1 block
#page-content-wrapper > div > div > div > div:nth-child(1) > div:nth-child(2) > div > div.visible-xs-block.visible-sm-block.planner-linear > div:nth-child(1) > ul.side-planner-list.semester-content-div-past.semester-content-div-1-1 > li:nth-child(2)

#page-content-wrapper > div > div > div > div:nth-child(1) > div:nth-child(2) > div > div.visible-xs-block.visible-sm-block.planner-linear > div:nth-child(1) > ul.side-planner-list.semester-content-div-past.semester-content-div-1-1 > li.list-heading > h1


# in 2 block
#page-content-wrapper > div > div > div > div:nth-child(1) > div:nth-child(2) > div > div.visible-xs-block.visible-sm-block.planner-linear > div:nth-child(1) > ul.side-planner-list.semester-content-div-past.semester-content-div-1-2 > li.list-heading > h1
#page-content-wrapper > div > div > div > div:nth-child(1) > div:nth-child(2) > div > div.visible-xs-block.visible-sm-block.planner-linear > div:nth-child(1) > ul.side-planner-list.semester-content-div-past.semester-content-div-1-2 > li:nth-child(2) > a > div.course-box-code

# retrived from javascript
all_pathway_url = [
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=30f8456d-ab3f-4fc5-a055-f0873e556154&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=d8967d99-cc5f-45a7-9672-cc1c2e000cdf&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=78991a0a-215a-4aad-800b-87b8f8958072&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=27af1858-889a-4c66-82f4-1ea5c12af8b6&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=d08c8b88-e987-4017-a065-48f927a3148f&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=2bb09dc5-f2a9-413e-a3d7-eeb9ab2a2abf&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=c3344b16-1015-4396-9823-1fb76b93c70f&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=5ec823f0-01b4-4933-9d2e-853ee2480636&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=7d3243c4-05b3-44af-89bf-71e4adc14227&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=49a80eb9-b883-48ce-86d2-814f3ca5ecd7&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=6ccd6350-09d1-4226-ad80-b3ca2f662f6b&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=dd8eb7e6-3fcb-4098-bba4-8b6b82b1208a&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=dadc47af-56f6-4ef9-9f0b-3ada16011343&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=91202fcb-b0ab-4cf9-bc0f-c5c46fd33a01&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=dd916540-e567-49f9-a664-f7dd98a97b9a&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=98446284-63c9-47c4-a727-cb1ebbc79e99&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=9bab79a0-fbb0-423e-b48d-083b92e9f815&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=98e01a1a-62e0-42ab-99c9-12ce46f026ee&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=3429f42f-b978-4928-9661-51902c4722a8&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=30c6efb5-14c4-4bcf-a330-21ff356769e7&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=31e2c40f-95fe-4822-aa63-e3de4e6887d9&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=e85751a5-bbf0-4886-b5fe-031540f8496a&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=c96c54d9-9aa3-4b2b-8bce-e8337a37c40d&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=9c054046-ce99-4d13-9111-344c24e984bf&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=09cc5f08-0b1d-4eb3-8309-a47e3d85d146&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=8041d2cb-66a9-4759-abb2-e7ffb8978c9b&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=0c0b010f-bb86-459b-8290-3cac2d4460ad&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=f4f84813-2361-4fe6-841a-613b25da6d93&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=ce709941-1b48-4ffb-b488-0f40372383f9&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=bbfcdd12-72e2-4e49-b464-d48b9a1fce46&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=014716e0-87d2-4012-b093-0886f081f3c3&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=ef6c7395-b2c1-4cf6-8eb9-07adf41f289d&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=ce0f3ab8-8b5e-4249-b1e9-555e02a29bee&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=73fc366e-e131-4597-9d40-9a940e20287c&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=4b4d23e0-cf73-4867-8ad7-86b4072c31bb&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=3d3232f2-59db-4d25-af50-6f93d6801c0f&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=f18f95f6-8f9c-4902-a0bb-2701b3661614&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=47169eb1-760f-469d-a86d-19433f47e8ee&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=1f7dbd44-8599-43a6-b1f8-749c33f738fd&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=b3c7865d-b58d-4502-8522-bf4794e6a0ad&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=49c1724e-e730-44bc-8a42-04f0d6606ad4&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=c593db55-3652-4e78-97fc-254aea7bbec4&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=b2eb989e-1eeb-4968-94f5-822e131c439d&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=96333547-c8d4-41a6-a34f-68da19f2b603&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=346a6fa4-7a72-43f4-af85-853808612fb4&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=8fec8826-f578-4b06-8f2f-5479bb2f0e19&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=e1c9c026-584c-4044-b5ab-cd430ec1d165&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=b36d5145-f6d4-4164-8eb5-3114865aabfe&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=13ec0c0b-4a57-4046-a8f4-0b770c94b82b&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=55d42b6d-746f-41f5-9d2c-4a7fefe5a081&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=c465f136-a66e-41d2-9a72-e933d9388307&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=aafa1d58-54bd-4e7e-a50b-d535bb93b380&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=fadf4ad1-ef01-4fd1-ba82-b177be0245b2&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=acabf397-494c-4be0-90e8-435b53af4063&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=7c0d9ce7-74eb-41ca-9e45-be77fe67c0a5&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=3b8dee6f-5387-4208-bc7e-94278ae6dcbf&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=ded08e2a-de7d-47f1-ab63-407a863d2878&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=967c49f0-ab79-4140-ad3b-6a8d90f859fb&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=1da7c42f-3fd4-4323-910e-eeec0ec4ddf0&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=317e4373-4fe8-43f4-89f1-5a6b2c778127&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=d547bac7-1f93-4a7e-a1c3-6890fe665464&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=79b2d5ab-1c35-4b8b-bf2b-e0bc4d49a1c4&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=5ec89aa7-71ff-4df2-b699-774fb66c594a&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=35e5a97d-173e-4a49-8799-02a8d931d5fa&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=cddca6ce-923e-4851-b90c-f3ab1acbe7aa&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=0f50f104-d798-4a5d-b800-42fa623bcd4b&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=7eacb0fc-4f44-4382-93c7-98731ee5b97c&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=f5bd70f9-b4b9-4bd2-beb5-c9c917d75b71&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=747d4bd8-326e-4a0d-8e8d-51d3a09ec9d7&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=92d76f15-05c4-44dc-ac3a-3e391fd66a89&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=fce30561-5ea4-4982-9197-fb0cab3e20ea&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=4fda256c-5f77-4043-9058-42b5ef8a48df&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=59e37444-ce12-4d9c-a37b-b489270546db&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=9725c9f8-d9de-4879-8f82-55cc37618368&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=408eda8a-846d-4421-a31f-9ede980076c0&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=8fd5e75c-01c9-4d15-aff4-47117f131706&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=911118d7-7618-4d0c-b8be-5064ac2876a3&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=250fea1a-e169-4155-b82a-897ef0c2c4ef&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=c579fc31-d104-45b9-a79f-7741c477ef0c&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=3de263ab-ccd0-433d-803c-41dbd1639ca2&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=8d91cb77-4b54-4355-a5d7-e5938f864960&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=2564679c-1b89-4e5f-8e08-7b3c07be6fb1&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=9038492f-f4bd-4210-9a06-fad910f5ae63&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=e1955f93-13aa-4ab9-8695-e16b6f44ecd5&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=79992e25-903c-4b8b-81d1-b8d6ec095db2&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=16388cd6-ed66-445a-a05e-0465ab05cfe8&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=38b37acd-0e59-4999-ab3a-b21a02df5650&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=12cea6b7-adcf-4420-a035-f632e2f07ec8&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=03700808-3d8f-4cf1-8edf-03c9a392b2e9&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=41a4eda8-dcd9-4358-a84f-14082ea856cc&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=1d9ff0f1-699a-467e-91b8-8fe93274b3b4&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=f9c25410-36a8-4578-9e13-0bfde7754901&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=6f69109b-d4b3-4019-96a0-c7e60eb8c137&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=e4eb9f92-b0b9-46a5-8393-7647eacb62a2&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=7d58e08c-e9de-4a2e-9dec-7573928decc4&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=a3dee6ef-e3dd-42c9-aab7-81687594eef7&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=dbabf700-c26f-4551-b225-504da0c7b7bb&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=d89aa435-e1f2-44a4-a256-65afac04dda0&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=7fe6c15a-a96a-433f-972c-79f101b21912&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=1ca5e6b0-eb1a-44ad-8931-38d627b54b8b&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=217f85c6-945b-43fd-966a-7dc456d73b2c&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=6ed8da97-7b7d-4a88-9682-24a32b0ae347&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=138682c1-e9e8-4aae-bd53-014ec4c62351&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=325ee71a-0ea0-4572-9520-dd86d6fb0f5d&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=84a4cd57-561b-4a75-b559-e740c6e169dd&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=d47a12b3-a5a5-48fe-8019-f55d779afa31&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=5579caf2-dc5d-4ae5-92fd-8bcfb0ded973&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=e46ca55f-1677-4ddb-8054-0ca942c380a1&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=c46ab1f8-9469-452c-a2f8-83ad7a5c3fe2&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=82657acb-a877-49fc-beb3-18dbfb243f01&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=32e5c23a-f491-4802-978d-c7781cb31ac5&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=6c87d43d-7e9e-4132-9037-f1f5651634e0&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=4f797ebb-6745-4ad8-bba1-47aa19f64be4&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=4dd9f8c7-bed3-41c2-838b-48b951c90c3e&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=5c57be96-97e9-462e-af1b-ede96236b554&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=4fb38a8d-7a9d-4c72-a010-dbf47ed685e3&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=ee17787b-8635-499b-9503-e64df5cb284f&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=c9a4c460-0896-4747-a175-ea53c155a3fd&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=e1d91259-f3bb-45a8-84bd-2ed595a05018&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=bb878e38-d771-4bd6-bffe-9255939c9305&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=8a8d9018-641b-4bba-8f18-c0dced7df7a5&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=5ac99603-bf44-488b-899f-51ba3f4ec0ff&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=c04b2762-cfb1-4a5a-acc5-5cf285a236cc&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=39be2353-7f6e-4be8-b118-fa9fa5a68271&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=4d0e88ad-96fa-4e87-949b-6ca155bf745b&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=390c6ea6-d6c5-49fa-a2e2-b4918cccabaf&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=2b81cc1b-597c-452a-a550-0753a450f3f4&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=8dd68b71-7629-42d4-9240-7a4083548125&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=61d9b184-c553-4b87-b347-23b6ff9ffd50&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=c57dcfe5-ff5e-4233-a6fe-08e707477052&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=e1fb655c-dcdb-40eb-97f3-15beb5a2e394&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=31d438de-dd87-4b08-8424-5fbf76b8d54f&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=3808a41c-e725-4dbb-8861-20ea10f8554b&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=46558e19-8956-475d-8317-8fe11657ad55&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=3fa1cd97-16a1-4cd9-828d-c5bc85692796&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=c65ca7a4-0ad3-49a5-89a6-e81449dfb28f&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=98bdd034-7193-4452-8d8b-90b27e094d89&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=b4d1b219-8eba-4d82-adc4-d5af94aefd22&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=59678779-3d7c-4609-a977-8654ec61c319&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=78d1bb6f-3c35-4afe-8481-b6eef0ddc663&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=8ba487fe-7dbd-47bd-b15a-5a35c013e046&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=f3e55be5-36d5-45c5-93d8-ebe6c9390a05&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=7b8bafe8-7921-43bc-ae9f-5d9ff9f62023&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=7d3cdcb4-1c3e-49c3-b017-4d65f53b39d2&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=28e3dd8e-8ca3-4939-a7e4-a4b3e1b0241a&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=8becdc86-9601-4625-98b7-8308cb8068e0&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=63fbdd13-c05b-4bdf-86ef-ef7771a5125a&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=9f67e42c-3e47-4d6c-874c-f2f6220af98c&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=d846872b-f820-48e1-95e3-303f1a7bcdca&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=e1174f04-c678-4e01-a3a3-7a43dfbd82aa&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=dae71635-afa9-43ff-ae66-2649c29ff1b1&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=16e95ea2-9466-474c-a108-014271512d2d&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=8606c7a7-811a-4df8-a3f0-1fce020c906a&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=07859396-58c4-4987-8af3-710a4219d2fd&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=c697e915-259b-481d-8c78-8d84349af62b&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=ee2b140a-deac-438e-ac5d-af3381c0e317&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=bf92cd68-f008-421e-bb32-9c2654d205df&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=f70e31dc-7f0f-4dbf-acc1-26200071d007&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=687a22d7-3133-48f7-8c34-8f913c482297&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=2bc7c95f-2c7c-4187-8a0f-749d6dbafff1&isTemplate=true",
    "https://academicaudit.andrew.cmu.edu/app/planner?plan_id=8b60a307-f45f-4dcf-b085-f54de42815e3&isTemplate=true",
]






# program name
# url
# course not in dashed block not in fall


driver = webdriver.Chrome(ChromeDriverManager().install())
init_url = all_pathway_url[0]
driver.get(init_url)
time.sleep(3)
username = driver.find_element_by_css_selector("#username")
password = driver.find_element_by_css_selector("#passwordinput")
username.send_keys("***") # your andrew
password.send_keys("***") # your password
driver.find_element_by_css_selector("#formwrapper > div:nth-child(4) > input").click()
time.sleep(20)


d = dict()
d["pathway"] = []
d["requiredY1"] = []
d["requiredY2"] = []
d["requiredY3"] = []
d["requiredY4"] = []
d["requiredY5"] = []
d["url"] = []


init_pathway_name = driver.find_element_by_css_selector("div.display-inline-block").text


#div-year-1 => fall
#div-year-2 => spring
#max-5 / check it by do max-6 again, if no difference, then max == 5
for init_yr in range(1,6):
    #import pdb
    #pdb.set_trace()
    try:
        init_year = driver.find_element_by_class_name("side-planner-list.semester-content-div-past.semester-content-div-"+str(init_yr)+"-2")
        init_required_course = init_year.find_elements_by_class_name("course-box-plan.box-plan.side-planner-req.ui-draggable-disabled")
        d["requiredY"+str(init_yr)].append([init_required_course[i].get_attribute('data-reqid') 
                        for i in range(len(init_required_course))])
        for init_other_yr in range(1,6):
            if init_other_yr != init_yr:
                d["requiredY"+str(init_other_yr)].append([])
        d["url"].append(init_url)
        d["pathway"].append(init_pathway_name)
    except:
        continue





for url in tqdm(all_pathway_url[1:]):
    driver.get(url) # no need to reenter login info
    time.sleep(6) # tuning to load all course info
    pathway_name = driver.find_element_by_css_selector("div.display-inline-block").text
    for yr in range(1,6):
        try:
            year = driver.find_element_by_class_name("side-planner-list.semester-content-div-past.semester-content-div-"+str(yr)+"-2")
            required_course = year.find_elements_by_class_name("course-box-plan.box-plan.side-planner-req.ui-draggable-disabled")
            d["requiredY"+str(yr)].append([required_course[i].get_attribute('data-reqid') 
                            for i in range(len(required_course))])
            for other_yr in range(1,6):
                if other_yr != yr:
                    d["requiredY"+str(other_yr)].append([])
            d["url"].append(url)
            d["pathway"].append(pathway_name)
        except:
            continue

#import pdb
#pdb.set_trace()

df = pd.DataFrame(d)
df.to_csv("working_matrix_withyrs.csv",index=False)
# enter a pass code button
# #passcode
# login keys auth_methods > fieldset > div.passcode-label.row-label > div > input
# click
# #passcode
# identify element
# driver.get("https://academicaudit.andrew.cmu.edu/app/planner?plan_id=30f8456d-ab3f-4fc5-a055-f0873e556154&isTemplate=true")
# time.sleep(5)





driver.close()
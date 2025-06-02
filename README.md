# AWS Cloud Services Hangman Game

A fun and educational word-guessing game where players try to guess AWS cloud service names one letter at a time before the hangman is complete.

## Features

- Multiple AWS service categories (Compute, Storage, Database, Networking, Security, etc.)
- Interactive letter selection
- Visual hangman drawing that builds with each wrong guess
- Score tracking
- Custom background image
- Clean and intuitive user interface

## How to Play

1. Click "Play Game" on the main menu
2. Select an AWS service category
3. Guess letters by clicking on the letter buttons
4. Try to guess the AWS service name before the hangman drawing is complete
5. You have 6 wrong guesses before the game ends
6. After each game, you can play again or return to the main menu

## AWS Categories Included

- **AWS Compute**: EC2, Lambda, Fargate, Lightsail, Beanstalk, Batch, ECS, EKS, Outposts, LocalZones
- **AWS Storage**: S3, EBS, EFS, FSx, Glacier, Snowball, Snowmobile, StorageGateway, Backup, DataSync
- **AWS Database**: RDS, DynamoDB, Aurora, Redshift, DocumentDB, Neptune, ElastiCache, Keyspaces, Timestream, QLDB
- **AWS Networking**: VPC, CloudFront, Route53, APIGateway, DirectConnect, GlobalAccelerator, TransitGateway, AppFabric, PrivateLink, CloudMap
- **AWS Security**: IAM, Cognito, GuardDuty, Inspector, Macie, Firewall, Shield, WAF, SecretsManager, KMS
- **AWS Analytics**: Athena, EMR, OpenSearch, Kinesis, Glue, QuickSight, DataZone, LakeFormation, MSK, DataExchange
- **AWS ML & AI**: SageMaker, Rekognition, Comprehend, Polly, Textract, Transcribe, Translate, Kendra, Bedrock, Lex
- **AWS Management**: CloudWatch, CloudTrail, Config, CloudFormation, Organizations, ControlCatalog, SystemsManager, TrustedAdvisor, CostExplorer, Chatbot

## Requirements

- Python 3.x
- Pygame

## Installation

1. Make sure you have Python installed
2. Install required packages:
   ```
   pip install pygame
   ```
3. Run the game:
   ```
   python hangman.py
   ```

## Game Controls

- Mouse click to select options and letters

## Customizing the Game

### Adding More AWS Services

You can easily add more AWS services to the game by editing the `custom_words.py` file:

```python
custom_categories = {
    "AWS Compute": ["EC2", "LAMBDA", ...],
    "AWS Storage": ["S3", "EBS", ...],
    # Add your own AWS category:
    "AWS New Category": ["SERVICE1", "SERVICE2", "SERVICE3", ...]
}
```

### Changing the Background Image

To change the background image:

1. Place your desired image in the `images` folder
2. Name the image `aws_bg.jpg`
3. The image will be automatically loaded when you start the game

## Folder Structure

```
hangman_game/
├── hangman.py         # Main game file
├── custom_words.py    # AWS service categories and names
├── README.md          # Documentation
├── images/            # Directory for images
│   └── aws_bg.jpg     # Background image
└── sounds/            # Directory for sound effects (optional)
```

## Educational Value

This game serves as a fun way to familiarize yourself with AWS service names across different categories, making it both entertaining and educational for cloud computing enthusiasts and AWS certification candidates.

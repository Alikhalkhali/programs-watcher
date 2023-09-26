<h2 align="center" >
  Table of Contents 
</h2>
<p align="center">
  <a href="#Installation">Installation</a> •
  <a href="#Configuring-Programs-Watcher">Configuring Programs Watcher</a> •
  <a href="#Contributing">Contributing</a> •
  <a href="#License">License</a> •
   <a href="#Contact">Contact</a> •
  </p>
  
# Programs Watcher
Programs Watcher is a Python program that monitors and notifies you of new updates from various bug bounty platforms. It uses MongoDB for data storage and Discord webhooks for notifications.
<br>
<br>
## Youtube Video

[![Video Thumbnail](https://github.com/Alikhalkhali/programs-watcher/blob/main/img/Thumbnail.jpg)](https://www.youtube.com/watch?v=V6d6_YVUSR8)
# Installation

To install Programs Watcher, follow these steps:

1. Clone the repository to your local machine:
```bash
git clone https://github.com/Alikhalkhali/programs-watcher.git
```
2. Change directory to the project folder:
```bash
cd programs-watcher
```
3. In the `config.yml` file, replace `<YOUR DISCORD WEBHOOK>` with your Discord webhook URL.
4. Run:
 ```bash
docker-compose up -d
```

# Configuring Programs Watcher

The Programs Watcher program uses a configuration file named `config.yml` to store information about the bug bounty platforms to monitor and the notification options to use.

## Discord Webhook

To use the Discord webhook, replace `<YOUR DISCORD WEBHOOK>` with the actual URL of your webhook in the following line:

```yaml
discordWebhook:
programs_watcher: <YOUR DISCORD WEBHOOK>
```

## MongoDB

- `uri`: This is the URI of the MongoDB database that the application will use to store data.
- `database`: This is the name of the database that the application will use to store data.

## Platforms

This section contains a list of bug bounty platforms to monitor. For each platform, provide the name, URL, and a set of notification options. The notification options specify which types of changes should trigger notifications.

### Monitor:

Specify the monitoring options for the platform.

- `rdp`: Set to true if you want to monitor RDP programs.
- `vdp`: Set to true if you want to monitor VDP programs.
- `excluded_programs`: List the URLs of the programs you wish to exclude from monitoring. Please note that this applies only to public programs.
- `specific_programs`:  List the specific program URLs you want to monitor. Note that it only monitors public programs. For example:
  - bugcrowd:
    ```yml
      specific_programs: 
        - https://bugcrowd.com/rarible-ogmbb
        - https://bugcrowd.com/smartthings
    ```
  - hackerone:
    ```yml
      specific_programs: 
        - https://hackerone.com/phabricator?type=team
        - https://hackerone.com/yahoo?type=team
    ```
  - intigriti:
    ```yml
      specific_programs: 
        - https://app.intigriti.com/programs/portofantwerp/nxtport
        - https://app.intigriti.com/programs/intergamma/intergamma
    ```
  - yeswehack:
    ```yml
      specific_programs: 
        - https://yeswehack.com/programs/swiss-post-evoting
        - https://yeswehack.com/programs/dana-bug-bounty-programd
    ```

### Notifications

To receive notifications for a specific type of change, set the corresponding notification option to `true`. The available notification options are:

- `new_program`: Notify when a new program is added.
- `removed_program`: Notify when a program is removed.
- `new_inscope`: Notify when a new scope is added.
- `removed_inscope`: Notify when a scope is removed.
- `new_out_of_scope`: Notify when a new out-of-scope item is added.
- `removed_out_of_scope`: Notify when an out-of-scope item is removed.
- `new_scope`: Notify when a scope is added or removed.
- `changed_scope`: Notify when a scope is modified.
- `new_type`: Notify when a new program type is added.
- `new_bounty_table`: Notify when a new bounty table is added.

Fill in the necessary information for each platform that you want to monitor.

# Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.

# License

This project is licensed under the MIT license. See the LICENSE file for details.

# Contact

If you have any questions or concerns, please feel free to contact me directly on social media:

- Twitter: [ali_khalkhali0](https://twitter.com/ali_khalkhali0)
- Instagram: [ali_khalkhali0](https://instagram.com/ali_khalkhali0)

I am always happy to hear from you and will do my best to respond to your questions as soon as possible.
<br>
#### For Support:

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/alikhalkhali)

# Programs Watcher

## Description

Programs Watcher is a Python program that monitors and notifies you of new updates from various bug bounty platforms. It uses MongoDB for data storage and Discord webhooks for notifications.

## Installation

To install Programs Watcher, follow these steps:

1. Clone the repository and navigate to the repository directory using your preferred method.
2. In the `config.yml` file, replace `<YOUR DISCORD WEBHOOK>` with your Discord webhook URL.
3. Run:
 ```bash
docker-compose up -d
```

## Configuring Programs Watcher

The Programs Watcher program uses a configuration file named `config.yml` to store information about the bug bounty platforms to monitor and the notification options to use.

### Discord Webhook

To use the Discord webhook, replace `<YOUR DISCORD WEBHOOK>` with the actual URL of your webhook in the following line:

```yaml
discordWebhook:
programs_watcher: <YOUR DISCORD WEBHOOK>
```

### MongoDB

- `uri`: This is the URI of the MongoDB database that the application will use to store data.
- `database`: This is the name of the database that the application will use to store data.

### Platforms

This section contains a list of bug bounty platforms to monitor. For each platform, provide the name, URL, and a set of notification options. The notification options specify which types of changes should trigger notifications.

#### Notifications

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

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT license. See the LICENSE file for details.

## Contact

If you have any questions or concerns, please feel free to contact me directly on social media:

- Twitter: [ali_khalkhali0](https://twitter.com/ali_khalkhali0)
- Instagram: [ali_khalkhali0](https://instagram.com/ali_khalkhali0)

I am always happy to hear from you and will do my best to respond to your questions as soon as possible.

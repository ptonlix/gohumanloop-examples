# GoHumanLoop Example with CrewAI

## Introduction

This example shows how to use the gohumanloop package to create a CrewAI agent that augments human control.

## Start

1. Create a .env file with your API key:

```bash
cp .env.example .env
# Modify the .env file with your API key and other configuration
```

2. Run the example:

```bash
uv run main.py
```

3. Check the mailbox where approval emails are received

<div align="center">
	<img height=360 src="http://cdn.oyster-iot.cloud/202505281625453.png"><br>
    <b face="雅黑"> View approval email </b>
</div>
<br>

4. Response to the email to approve or reject the request

According to the guidelines, reply to messages of agreement or refusal in the format provided

```
===== PLEASE KEEP THIS LINE AS CONTENT START MARKER =====
Decision: approve
Reason: [Your reason]
===== PLEASE KEEP THIS LINE AS CONTENT END MARKER =====
```

<div align="center">
	<img height=240 src="http://cdn.oyster-iot.cloud/202505281636951.png"><br>
</div>
<br>

Approved and completed the task.

## License

This project is released under the MIT License.

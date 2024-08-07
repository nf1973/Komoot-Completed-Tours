# Komoot Completed Tours

Extract your completed tours from Komoot to a local JSON file.

## Usage

### 1. Find your Komoot User ID / User Number

- Log into Komoot and go to your Profile page.
- At the end of the URL you will see your user id / number.

_Note: This is a **number**, not your e-mail adddress_

**Optionally:** You can create a file called `user_id.dat` (in the same folder as`extracttours.py`) and paste in your user id, **or** you can type/paste it when prompted to do so.

### 2. Copy your cookies

- Go to your Completed Tours page, and open the Developer Tools in your browser.

- Switch to the Network tab of the Developer Tools and show the "Fetch/XHR" requests

- Scroll down a bit and you will see some requests with the name starting with "tours/?sport_types=" appear

- Click on on of these requests and go to Headers / Request Headers section, then look for the "Cookie:" key.

- Copy the **entire** value of the Cookie key (it will start with `_stripe` and end with &
  `expire=1723062677369` - _the number will be different_)

* **Optionally:** You can create a file called `cookie.dat` (in the same folder as `extracttours.py`) and paste in your cookies, **or** you can paste it when prompted to do so.

_Note: If you choose to paste the cookies when prompted, you may first have to increase the size of your terminal's paste buffer in order to ensure the entire cookie can be pasted in._

**Important: Your cookie will expire after about 10 mins. If it has expired, you will need to repeat the whole of Step 2.**

### 3. Run the script to extract your completed tours

To run the script, run:

```
python3 extracttours.py
```

- The first time you run the script, a file called `tours.json`will be created in the same folder as the script, and all of your completed tours will be added.

- When subsequently re-running the script, only new tours not already in the file will be added.

- If you delete `tours.json` it will be recreated with all tours the next time you run the script.

If you run into any issues, please report in the Issues Section of the repository at https://github.com/nf1973/Komoot-Completed-Tours

# Tandem Mode hardware check

Status: **user-confirmed working in-game on 2026-09-13** using the current
v0.1.1 executable, a primary Stadia controller, and a PlayStation secondary
controller. The user connected the PlayStation controller for this test and
reported that it worked fine in the game. The exact PlayStation model and game
were not recorded. No app changes or Tandem toggle were needed.

The separate automated observation saw one Xbox slot with idle values during
its sampling window; it did not independently capture the secondary controls.
This is a user-reported in-game result, not a completed run of every check below.
Simultaneous opposing controls, secondary disconnect/reconnect, and other models
remain unverified. The primary controller combines inputs as described in
[Google’s documentation](https://support.google.com/stadia/answer/13067284?hl=en-GB).

Use the README’s Tandem setup first, then test the running EXE:

- Open **Test in Windows**, choose the virtual Xbox controller, and open Properties.
- Leave the primary untouched and test the secondary’s buttons, sticks, and triggers.
- Leave the secondary untouched and repeat on the primary.
- Hold A on the primary and a different button on the secondary. Confirm that the
  same Xbox device receives both. Release them and check that neither stays held.
- Disconnect the secondary while holding a button. Confirm that it releases and
  the primary still works. Reconnect and test again.
- Use Stop and Start in the app and confirm the pair still shares one Xbox output.

Record Windows version, primary firmware/connection, secondary model, cable or
adapter, and observed results. Do not count a unit test with simulated input as
physical Tandem verification. Opposing stick inputs are combined by the controller
firmware; the bridge does not choose an arbitration policy.

# Seeed SenseCAP Indicator D1L

Experimental support for the **GX/ST7701S display variant** of the Seeed SenseCAP Indicator D1L,
SKU 114993070. The profile covers **Wi-Fi, the 480×480 RGB display, capacitive touch and backlight**.
It does not enable LoRa or reprogram the RP2040.

## Hardware and variant limits

The Indicator contains an ESP32-S3 with 8 MB octal PSRAM and 8 MB flash, plus a separate RP2040.
The display and touch are connected to the ESP32. Grove, SD and the buzzer belong to the RP2040
and are not exposed by this profile. There is no battery.

Seeed's SDK distinguishes GX (SPI initialization plus RGB, ST7701S) and DX (RGB-only) panels,
including for its D1L board option. This profile uses ESPHome's native
`mipi_rgb` model `SEEED-INDICATOR-D1` and the GX touch address **0x48**.
It does not establish compatibility with DX panels, other Indicator variants or the separate
Meshtastic product. Check the actual label and hardware revision before installing.

The D1L is the LoRa variant, not the D1S environmental-sensor variant. Product-family descriptions
do not establish which sensors are fitted to a particular unit.

## Configuration

- Board key: **sensecapd1l**.
- Board file: `packages/boards/seeed-sensecap-indicator-d1l.yaml`.
- Checkout entry: `checkout/sensecapd1l.yaml`, generated from `boards.yaml`.
- Standard look at 171.85 dpi, rounded to 172 dpi in catalog metadata.
- Default 2×3 grid and the conservative core limits of 64 tiles across 8 pages.
- LVGL draw buffer 12%, an eighth of the frame under the ESPHome buffer rules.
- Octal PSRAM 80 MHz and shared S3-RGB hardware settings.
- No camera-picture or snapshot feature enabled in this initial profile.

These limits preserve the initial hardware configuration rather than claiming the capacity of
other S3 boards. A larger or image-heavy layout requires separate memory and stability validation.

### Wiring

| Function | ESP32 GPIO or PCA9535 bit |
|---|---|
| I2C SDA / SCL | GPIO39 / GPIO40 |
| 16-bit expander | I2C 0x20, native `pca9554` with `pin_count: 16` |
| LCD SPI clock / MOSI | GPIO41 / GPIO48 |
| LCD CS / reset | Expander 4 / 5 |
| Touch | FT6336U via `ft5x06`, I2C 0x48 |
| Touch reset | Expander 7, held high |
| Backlight | GPIO45, active high, LEDC 100 Hz |
| Unused LoRa CS | Expander 0, held high to deselect the radio |
| RP2040 reset | Expander 8, not configured |

The native display preset supplies the RGB data pins and porches; pixel clock is 16 MHz.
Touch polls every 20 ms because its interrupt is on expander bit 6, not an internal ESP32 GPIO.
Both touch axes are mirrored to match the display preset. Do not add a second correction in LVGL.
The backlight frequency is available as `BACKLIGHT_FREQUENCY` in Override YAML.

The shared backlight feature supplies brightness, standby and night controls.
Frequency, dimming quality, standby/wake and behavior after a power interruption still need
broader hardware acceptance. The initial profile does not bind the physical user button.

## Installation and recovery

Use `checkout/sensecapd1l.yaml` for a build from this clone, following [checkout/README.md](../checkout/README.md).
The generated remote entry is for publication with the project, not evidence that an unpublished branch
can already be installed from the default GitHub branch. A local branch does not change an installed
Screen Manager or publish a new board to it.

The Indicator exposes two USB serial interfaces through a hub. Seeed documents CH340 for the ESP32,
and a separate RP2040 USB interface which may report `INDICATOR RP2040`.
Identify the target by USB metadata and confirm ESP32-S3 before writing.
COM numbers are machine-dependent; never choose a port solely by its number.

Only the ESP32 is programmed by this profile. Preserve a private full flash backup and check a
revision-appropriate recovery route before replacing existing firmware. A firmware image or backup
may contain credentials. The external button's factory reset behavior is firmware behavior, not a
guaranteed way to reinstall the original firmware.

This board uses 8 MB flash and ESPHome's corresponding partition layout, not the project's special 4 MB
migration layout. Changes to partition tables or recovery images need separate validation.
Do not install Meshtastic firmware on an incompatible Indicator.

## Acceptance scope

The originating local proof of concept exercised Wi-Fi, visible display output, touch at the
four corners, the real Tessera/LVGL settings interface, Home Assistant pairing, runtime tile delivery
and lamp control. This is limited proof on an individual setup, not a guarantee for every hardware revision.

The catalog integration and generated checkout entry are a separate packaging step.
Rotation, cold boot, settings persistence, dimming/standby, firmware updates, sustained load and
the oldest supported ESPHome version still need acceptance on the final packaged profile.
The board remains experimental.

## Primary references

- [Seeed D1L product PDF, SKU114993070](https://files.seeedstudio.com/Bazaar/product_pdf/114993070.pdf).
- [Seeed hardware diagram](https://files.seeedstudio.com/wiki/SenseCAP/SenseCAP_Indicator/SenseCAP_Indicator_6.png).
- [Seeed SDK panel selection](https://github.com/Seeed-Solution/SenseCAP_Indicator_ESP32/blob/77edb8d2b9a92fc67965c1b2d4a838f0d09a1800/components/bsp/Kconfig.projbuild).
- [ESPHome 2026.9.0 native display preset](https://github.com/esphome/esphome/blob/2026.9.0/esphome/components/mipi_rgb/models/st7701s.py).
- [Published ESPHome Indicator configuration](https://devices.esphome.io/devices/seeed-sensecap/).
- [Seeed firmware recovery documentation](https://wiki.seeedstudio.com/SenseCAP_Indicator_How_To_Flash_The_Default_Firmware/).

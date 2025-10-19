# Company Invoice QR Image Module

This Odoo 17 module adds a configurable QR image field to the company (res.company) model and displays it on customer invoice PDFs.

## Features

- **Binary field for QR image** in the company form view
- **QR image display** on invoice reports below company information
- **Clean and configurable** implementation
- **Responsive design** with proper styling

## Installation Steps

### 1. Module Installation

1. Copy the `abp_invoice_qr` module to your Odoo addons directory
2. Update the addons list in Odoo:
   - Go to Apps → Update Apps List
3. Install the module:
   - Search for "Company Invoice QR Image" in Apps
   - Click Install

### 2. Configuration

1. **Configure QR Image**:
   - Go to Settings → Companies → Companies
   - Open your company form
   - You'll see a new "Invoice QR Image" field below the company logo
   - Upload your QR code image (recommended size: 120x120 pixels)

2. **Test the Implementation**:
   - Create or open a customer invoice
   - Print the invoice as PDF
   - The QR image should appear below the company information

## Technical Details

### Files Structure

```
company_invoice_qr/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── res_company.py
├── views/
│   └── res_company_views.xml
├── reports/
│   └── invoice_report.xml
├── security/
│   └── ir.model.access.csv
└── README.md
```

### Key Components

1. **Model Extension** (`models/res_company.py`):
   - Adds `invoice_qr_image` binary field to `res.company`

2. **View Extension** (`views/res_company_views.xml`):
   - Adds QR image field to company form view
   - Uses image widget with 90x90 size options

3. **Report Extension** (`reports/invoice_report.xml`):
   - Inherits from `account.report_invoice_document`
   - Displays QR image below payment communication
   - Responsive styling with max 125x125 pixels

### Dependencies

- `base`: Core Odoo functionality
- `account`: Invoice reporting functionality

## Usage Notes

- **Image Format**: Supports all standard image formats (PNG, JPG, GIF, etc.)
- **Image Size**: Recommended 120x120 pixels for optimal display
- **Display Location**: QR image appears below company information on invoices
- **Conditional Display**: QR image only shows if uploaded (conditional rendering)

## Troubleshooting

### QR Image Not Displaying
- Ensure the image is uploaded in the company form
- Check that the invoice is using the standard invoice report template
- Verify the module is properly installed and updated

### Image Quality Issues
- Use high-resolution images (at least 120x120 pixels)
- Ensure good contrast for QR code readability
- Test with different image formats if needed

## Support

For issues or questions regarding this module, please contact the development team.

## License

This module is licensed under LGPL-3.

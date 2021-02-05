# slice_order_philips
This is currently quite unverified and may not produce accurate slice orders

To run:

`python philips_dicom_sliceorder.py dicom_file.dcm`


Because of rounding issues, you may need to touch up the ordering by hand.

This is a python3 implementation of  http://www.onerussian.com/tmp/philips_order.py with a few changes (using datetime to process the times in the file and not relying on the first timepoint (which seems less interpretable than others))

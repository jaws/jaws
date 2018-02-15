def write_data(args, ds, op_file, encoding):
	if args.format3 == 1:
		ds.to_netcdf(op_file, format = 'NETCDF3_CLASSIC', unlimited_dims={'time':True}, encoding = encoding)
	elif args.format4 == 1:
		ds.to_netcdf(op_file, format = 'NETCDF4', unlimited_dims={'time':True}, encoding = encoding)
	elif args.format5 == 1:
		ds.to_netcdf(op_file, format = 'NETCDF3_64BIT', unlimited_dims={'time':True}, encoding = encoding)
	elif args.format6 == 1:
		ds.to_netcdf(op_file, format = 'NETCDF3_64BIT', unlimited_dims={'time':True}, encoding = encoding)
	elif args.format7 == 1:
		ds.to_netcdf(op_file, format = 'NETCDF4_CLASSIC', unlimited_dims={'time':True}, encoding = encoding)
	else:
		ds.to_netcdf(op_file, unlimited_dims={'time':True}, encoding = encoding)

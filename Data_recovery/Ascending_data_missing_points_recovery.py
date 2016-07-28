prev_num_in_seq = 0
cur_num_in_seq = 0
last_good_data = 0
counter = 0

# Open the text file with specified name and use for loop until EOF
with open('test.txt', 'r') as instrument_readings:
    for index, line in enumerate(instrument_readings):
        # Read the number in the line
        cur_num_in_seq = int(line)
        if index == 0:
            prev_num_in_seq = 0


        # Normal operation, numbers are growing
        if prev_num_in_seq < cur_num_in_seq:
            # print "counter" + str(counter)
            # Open file in append mode
            corrected_seq = open('corr_seq.txt', 'a')
            # If there was a repeating sequence, create artificial
            # values and write them into file
            if counter > 0 or last_good_data != 0:
                print cur_num_in_seq, last_good_data
                # Difference between new good data and old repeating data
                diff = cur_num_in_seq - prev_num_in_seq
                step_size = float(float(diff)/float((counter + 1)))
                print "Step_size " + str(step_size) + " diff " + str(diff)
                print range(counter)
                for step_incr in range(counter):
                    if step_incr == 0:
                        float_value = prev_num_in_seq + step_size
                    elif step_incr == 1:
                        float_value = prev_num_in_seq + step_size*2
                    else:
                        float_value = prev_num_in_seq + step_size*step_incr
                    print "Artif value" + str(float_value)
                    # print float_value
                    corrected_seq.write(str(float_value) + "\n")
                corrected_seq.write(str(cur_num_in_seq) + "\n")
                last_good_data = 0
                counter = 0
            # Record values as normal
            else:
                print "Regular value" + str(cur_num_in_seq)
                # Appending automatically takes care of the index
                corrected_seq.write(str(cur_num_in_seq) + "\n")
        # Data has been captured with errors, duplicate data
        else:
            print 'Repeating' + str(cur_num_in_seq)
            if last_good_data == 0:
                last_good_data = cur_num_in_seq
            counter = counter + 1
            print 'Counter ' + str(counter) 
            
        # Save the current value for the next loop 
        prev_num_in_seq = cur_num_in_seq
    
    else:
        print "Data is repaired"
        instrument_readings.close()

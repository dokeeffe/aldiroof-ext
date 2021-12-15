<!DOCTYPE html>
<html>
<head>
    <title>Observatory Roof</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
    <![endif]-->
</head>
<body>
<div class="container">
<h1>Obs Roof <span id="state">Loading....</span></h1>
    <div class="container">
        <div class="row justify-content-between">
            <div class="col-4">
                <button type="button" id="openroof" data-loading-text="Opening..." class="btn btn-primary" autocomplete="off">Open</button>
            </div>
            <div class="col-4">
                <button type="button" id="abort" data-loading-text="Opening..." class="btn btn-warning" autocomplete="off">Abort</button>
            </div>
            <div class="col-4">
                <button type="button" id="closeroof" data-loading-text="Closing..." class="btn btn-primary" autocomplete="off">Close</button>
            </div>
        </div>
    </div>
</div>

<script src="http://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
<script>
    $(document).ready(function () {
      refresh();

      $('#openroof').on('click', function () {
          $('#state').text('Opening')
          $.post( 'open', function( openresp ) {
            set_roof_state(openresp);
          });
        });
      $('#abort').on('click', function () {
          $('#state').text('Aborting')
          $.post( 'abort', function( resp ) {
            set_roof_state(resp);
          });
        });
      $('#closeroof').on('click', function () {
          $('#state').text('Closing') 
          $.post( 'close', function( resp ) {
            set_roof_state(resp);
          });
        });
    });

    function refresh() {
        $.get( 'roof', function( data ) {
          set_roof_state(data);
      }).fail(function() {
          alert('failed')
      });
      setTimeout(refresh, 5000);
    }

    function set_roof_state(json) {
        $('#state').text(json.state);
        $('#closeroof').prop('disabled', false);
        $('#openroof').prop('disabled', false);
        if(json.state=='CLOSED') {         
            $('#closeroof').prop('disabled', true);
        }
        if(json.state=='OPEN') {
            $('#openroof').prop('disabled', true);
        }
    }
</script>
</body>
</html>

from django.test import TestCase
from django.urls import reverse
from mercury.models import EventCodeAccess
from ag_data.models import AGSensor, AGSensorType


class TestConfigureSensorView(TestCase):
    TESTCODE = "testcode"

    login_url = "mercury:EventAccess"
    sensor_url = "mercury:sensor"

    test_sensor_name = "live-feed"
    field_name_1 = "test-field-1"
    field_name_2 = "test-field-2"
    data_type_1 = "test-data-type-1"
    data_type_2 = "test-data-type-2"
    unit_1 = "test-unit-1"
    unit_2 = "test-unit-2"

    test_sensor = {
        "name": test_sensor_name,
        "processing formula": 0,
        "field-names": [field_name_1, field_name_2],
        "data-types": [data_type_1, data_type_2],
        "units": [unit_1, unit_2],
    }

    def setUp(self):
        test_code = EventCodeAccess(event_code="testcode", enabled=True)
        test_code.save()

    def _get_with_event_code(self, url, event_code):
        self.client.get(reverse(self.login_url))
        self.client.post(reverse(self.login_url), data={"eventcode": event_code})
        response = self.client.get(reverse(url))
        session = self.client.session
        return response, session

    def test_configure_sensor_view_get_success(self):
        response, session = self._get_with_event_code(self.sensor_url, self.TESTCODE)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(True, session["event_code_known"])

    # Adding New Sensor Tests

    # Valid
    # Valid POST to create sensor returns status OK
    def test_configure_sensor_valid_POST_add_new_sensor_returns_status_ok(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data
        response = self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_sensor": "",
                "sensor-name": self.test_sensor["name"],
                "field-names": self.test_sensor["field-names"],
                "data-types": self.test_sensor["data-types"],
                "units": self.test_sensor["units"],
            },
        )

        # Check that POST redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    # Valid POST creates new AGSensor & AGSensorType object
    def test_configure_sensor_valid_post_add_new_sensor_success_object_created(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST good sensor data
        self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_sensor": "",
                "sensor-name": self.test_sensor["name"],
                "field-names": self.test_sensor["field-names"],
                "data-types": self.test_sensor["data-types"],
                "units": self.test_sensor["units"],
            },
        )

        # Check that AGSensor & AGSensorType object is created in db with expected params
        sensors = AGSensor.objects.all()
        sensor_types = AGSensor.objects.all()
        self.assertEqual(sensors.count(), 1)
        self.assertEqual(sensor_types.count(), 1)

    # Invalid
    # Invalid POST name conflict with existing AGSensor returns status ok
    def test_configure_sensor_invalid_POST_add_new_sensor_duplicate_name_returns_status_ok(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        test_type_object = AGSensorType.objects.create(
            name="TEST",
            processing_formula=0,
            format={
                self.field_name_1: {"data_type": self.data_type_1, "unit": self.unit_1},
                self.field_name_2: {"data_type": self.data_type_1, "unit": self.unit_1},
            },
        )
        test_type_object.save()

        test_sensor_object = AGSensor.objects.create(
            name=self.test_sensor["name"], type_id=test_type_object
        )
        test_sensor_object.save()
        # POST sensor data
        response = self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_sensor": "",
                "sensor-name": self.test_sensor["name"],
                "field-names": self.test_sensor["field-names"],
                "data-types": self.test_sensor["data-types"],
                "units": self.test_sensor["units"],
            },
        )

        # Check that POST redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    # Invalid POST name conflict with existing AGSensor no object created
    def test_configure_sensor_invalid_POST_add_new_sensor_duplicate_name_not_created(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        test_type_object = AGSensorType.objects.create(
            name="TEST",
            processing_formula=0,
            format={
                self.field_name_1: {"data_type": self.data_type_1, "unit": self.unit_1},
                self.field_name_2: {"data_type": self.data_type_1, "unit": self.unit_1},
            },
        )
        test_type_object.save()

        test_sensor_object = AGSensor.objects.create(
            name=self.test_sensor["name"], type_id=test_type_object
        )
        test_sensor_object.save()
        # POST sensor data
        response = self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_sensor": "",
                "sensor-name": self.test_sensor["name"],
                "field-names": self.test_sensor["field-names"],
                "data-types": self.test_sensor["data-types"],
                "units": self.test_sensor["units"],
            },
        )

        # Check that AGSensor & AGSensorType objects are not created
        sensors = AGSensor.objects.all()
        sensor_types = AGSensorType.objects.all()

        self.assertEqual(sensors.count(), 1)
        self.assertEqual(sensor_types.count(), 1)

    # Invalid POST name conflict with existing AGSensorType returns status ok
    def test_configure_sensor_invalid_POST_add_new_sensor_duplicate_type_name_returns_status_ok(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        test_type_object = AGSensorType.objects.create(
            name=self.test_sensor["name"],
            processing_formula=0,
            format={
                self.field_name_1: {"data_type": self.data_type_1, "unit": self.unit_1},
                self.field_name_2: {"data_type": self.data_type_1, "unit": self.unit_1},
            },
        )
        test_type_object.save()
        # POST sensor data
        response = self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_sensor": "",
                "sensor-name": self.test_sensor["name"],
                "field-names": self.test_sensor["field-names"],
                "data-types": self.test_sensor["data-types"],
                "units": self.test_sensor["units"],
            },
        )

        # Check that POST redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    # Invalid POST name conflict with existing AGSensorType object not created
    def test_configure_sensor_invalid_POST_add_new_sensor_duplicate_type_name_not_created(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        test_type_object = AGSensorType.objects.create(
            name=self.test_sensor["name"],
            processing_formula=0,
            format={
                self.field_name_1: {"data_type": self.data_type_1, "unit": self.unit_1},
                self.field_name_2: {"data_type": self.data_type_1, "unit": self.unit_1},
            },
        )
        test_type_object.save()
        # POST sensor data
        response = self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_sensor": "",
                "sensor-name": self.test_sensor["name"],
                "field-names": self.test_sensor["field-names"],
                "data-types": self.test_sensor["data-types"],
                "units": self.test_sensor["units"],
            },
        )

        # Check that AGSensor & AGSensorType objects are not created
        sensors = AGSensor.objects.all()
        sensor_types = AGSensorType.objects.all()
        self.assertEqual(sensors.count(), 0)
        self.assertEqual(sensor_types.count(), 1)

    # Invalid POST missing name returns status OK
    def test_configure_sensor_invalid_POST_add_new_sensor_missing_name_returns_status_ok(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data
        response = self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_sensor": "",
                "sensor-name": "",
                "field-names": self.test_sensor["field-names"],
                "data-types": self.test_sensor["data-types"],
                "units": self.test_sensor["units"],
            },
        )

        # Check that POST redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    # Invalid POST missing name doesn't create objects
    def test_configure_sensor_invalid_POST_add_new_sensor_missing_name_not_created(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data
        response = self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_sensor": "",
                "sensor-name": "",
                "field-names": self.test_sensor["field-names"],
                "data-types": self.test_sensor["data-types"],
                "units": self.test_sensor["units"],
            },
        )

        # Check that AGSensor & AGSensorType objects are not created
        sensors = AGSensor.objects.all()
        sensor_types = AGSensor.objects.all()
        self.assertEqual(sensors.count(), 0)
        self.assertEqual(sensor_types.count(), 0)

    # Invalid POST missing field name returns status OK
    def test_configure_sensor_invalid_POST_add_new_sensor_missing_field_names_returns_status_ok(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data
        response = self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_sensor": "",
                "sensor-name": self.test_sensor["name"],
                "field-names": "",
                "data-types": self.test_sensor["data-types"],
                "units": self.test_sensor["units"],
            },
        )

        # Check that POST redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    # Invalid POST missing field name doesn't create objects
    def test_configure_sensor_invalid_POST_add_new_sensor_missing_field_names_not_created(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data
        response = self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_sensor": "",
                "sensor-name": self.test_sensor["name"],
                "field-names": "",
                "data-types": self.test_sensor["data-types"],
                "units": self.test_sensor["units"],
            },
        )

        # Check that AGSensor & AGSensorType objects are not created
        sensors = AGSensor.objects.all()
        sensor_types = AGSensor.objects.all()
        self.assertEqual(sensors.count(), 0)
        self.assertEqual(sensor_types.count(), 0)

    # Invalid POST duplicate field names returns status OK
    def test_configure_sensor_invalid_POST_add_new_sensor_duplicate_field_names_returns_status_ok(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data
        response = self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_sensor": "",
                "sensor-name": self.test_sensor["name"],
                "field-names": [self.field_name_1, self.field_name_1],
                "data-types": self.test_sensor["data-types"],
                "units": self.test_sensor["units"],
            },
        )

        # Check that POST redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    # Invalid POST duplicate field names objects not created
    def test_configure_sensor_invalid_POST_add_new_sensor_duplicate_field_names_returns_status_ok(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data
        response = self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_sensor": "",
                "sensor-name": self.test_sensor["name"],
                "field-names": [self.field_name_1, self.field_name_1],
                "data-types": self.test_sensor["data-types"],
                "units": self.test_sensor["units"],
            },
        )

        # Check that AGSensor & AGSensorType objects are not created
        sensors = AGSensor.objects.all()
        sensor_types = AGSensor.objects.all()
        self.assertEqual(sensors.count(), 0)
        self.assertEqual(sensor_types.count(), 0)
